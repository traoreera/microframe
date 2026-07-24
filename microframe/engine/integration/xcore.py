import asyncio
from pathlib import Path
from typing import Any, Optional

from ..cache import CacheBackend
from ..core.renderer import TemplateEngine

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
    from xcore import Xcore
    from xcore.services.cache import CacheService
except ImportError:
    FastAPI = None  # type: ignore
    StaticFiles = None  # type: ignore
    Xcore = None  # type: ignore
    CacheService = None  # type: ignore


class XCoreCacheBackend(CacheBackend):
    """Bridge microframe cache → xcore CacheService."""

    def __init__(self, cache_service: "CacheService"):
        self._cache = cache_service

    def get(self, key: str, ttl: Optional[int] = None) -> Optional[Any]:
        try:
            return asyncio.run(self._cache.get(key))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._cache.get(key))
            finally:
                loop.close()

    def set(self, key: str, value: Any):
        try:
            asyncio.run(self._cache.set(key, value))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._cache.set(key, value))
            finally:
                loop.close()

    def delete(self, key: str):
        try:
            asyncio.run(self._cache.delete(key))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._cache.delete(key))
            finally:
                loop.close()

    def clear(self):
        try:
            asyncio.run(self._cache.clear())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._cache.clear())
            finally:
                loop.close()


class XCoreStatic:
    """Builds static URLs using xcore's mount path + asset versioning.

    Usage:
        engine.add_global("static", XCoreStatic(mount_prefix="/static"))
    """

    def __init__(self, mount_prefix: str = "/static", asset_versions: Optional[dict] = None):
        self._prefix = mount_prefix.rstrip("/")
        self._versions = asset_versions or {}

    def set_version(self, path: str, version: str):
        self._versions[path] = version

    def __call__(self, path: str) -> str:
        version = self._versions.get(path, "")
        url = f"{self._prefix}/{path}"
        if version:
            url += f"?v={version}"
        return url


_action_map: dict = {}


async def _make_remote_caller(xcore_instance: "Xcore"):
    """Return an async function that calls xcore plugins via internal IPC."""

    async def _call(name: str, kwargs: dict) -> Optional[str]:
        try:
            plugin, action = name.split(".", 1)
        except ValueError:
            return None
        try:
            result = await xcore_instance.plugins.call(plugin, action, kwargs)
            if isinstance(result, dict):
                return result.get("html") or result.get("result") or str(result)
            return str(result) if result else None
        except Exception:
            return None

    return _call


def _make_action_resolver():
    """Return a function that generates opaque action URLs."""

    import secrets

    def _resolve(name: str, kwargs: dict) -> str:
        token = secrets.token_hex(16)
        try:
            plugin, action = name.split(".", 1)
        except ValueError:
            return "#"
        _action_map[token] = (plugin, action)
        return f"/_/a/{token}"

    return _resolve, _action_map


def create_xcore_engine(
    xcore_instance: "Xcore",
    directory: str = "templates",
    enable_ui: bool = False,
    enable_minify: bool = True,
    enable_cache: bool = False,
    cache_ttl: int = 300,
    debug: bool = True,
    static_prefix: str = "/static",
    **kwargs,
) -> TemplateEngine:
    """Create a TemplateEngine wired to xcore services.

    - Cache → xcore's CacheService (if available)
    - remote/action → xcore plugin calls with opaque URLs
    - static() → XCoreStatic with xcore-aware prefix
    """
    import asyncio

    container = getattr(xcore_instance, "services", None)
    cache_backend = None

    if container and container.has("cache"):
        cache_service = container.get("cache")
        cache_backend = XCoreCacheBackend(cache_service)
        enable_cache = True

    remote_caller = asyncio.run(_make_remote_caller(xcore_instance))
    action_resolver, _ = _make_action_resolver()

    engine = TemplateEngine(
        directory=directory,
        debug=debug,
        enable_minify=enable_minify,
        enable_cache=enable_cache,
        enable_ui=enable_ui,
        cache_ttl=cache_ttl,
        cache_backend=cache_backend,
        remote_caller=remote_caller,
        action_resolver=action_resolver,
        **kwargs,
    )

    static_helper = XCoreStatic(
        mount_prefix=static_prefix,
        asset_versions=engine._asset_versions,
    )
    engine.add_global("static", static_helper)

    return engine


def register_action_routes(app: "FastAPI", prefix: str = "/_/a"):
    """Register the opaque action handler on a FastAPI app.

    Routes POST /_/a/<token> → plugin action lookup → execute.
    Validates CSRF token and redirect or returns HTML.
    """
    if not FastAPI:
        raise ImportError("fastapi is required: pip install microframe[xcore]")

    from fastapi import Form, Request
    from fastapi.responses import HTMLResponse, RedirectResponse

    @app.post(prefix + "/{token}")
    async def handle_action(token: str, request: Request):
        entry = _action_map.get(token)
        if not entry:
            return HTMLResponse("<!-- invalid action -->", status_code=404)

        plugin, action = entry
        form = await request.form()
        form_data = dict(form)

        # Validate CSRF
        csrf_token = form_data.pop("csrf_token", "")
        redirect = form_data.pop("redirect", "")

        engine = None
        for _, service in getattr(request.app.state, "services", {}).items():
            if hasattr(service, "env"):
                engine = service
                break

        if engine:
            expected = engine.env.globals.get("csrf_token", lambda: "")()
            if csrf_token != expected:
                return HTMLResponse("<!-- csrf invalid -->", status_code=403)

        from xcore import Xcore
        xcore: Xcore = getattr(request.app, "_xcore_instance", None)
        if xcore:
            result = await xcore.plugins.call(plugin, action, form_data)
            if isinstance(result, dict):
                result = result.get("html") or result.get("result", "")

        if redirect:
            return RedirectResponse(url=redirect, status_code=303)
        return HTMLResponse(str(result or ""))


def mount_template_static(
    app: "FastAPI",
    template_dir: str,
    url_prefix: str = "/static",
    name: str = "static",
):
    """Mount a template directory's static/ folder onto a FastAPI app.

    If ``template_dir/static/`` exists, it is served at ``url_prefix``.
    """
    if not StaticFiles:
        raise ImportError("fastapi is required: pip install microframe[xcore]")

    static_path = Path(template_dir) / "static"
    if static_path.is_dir():
        app.mount(url_prefix, StaticFiles(directory=str(static_path)), name=name)


def register_engine_service(
    xcore_instance: "Xcore",
    engine: TemplateEngine,
    service_name: str = "template_engine",
):
    """Register a TemplateEngine as an xcore service so plugins can access it.

    Usage in a plugin:
        engine = await self.get_service("template_engine")
        html = await engine.render("page.html", ctx)
    """
    if not hasattr(xcore_instance, "services"):
        return

    container = xcore_instance.services
    container.register_service(service_name, engine)
