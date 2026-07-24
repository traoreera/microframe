"""Integration with xcore (https://github.com/traoreera/xcore).

MicroFrame plugs into xcore as a real xcore *extension* (`BaseService`),
declared in `xcore.yaml` under `services.extensions`. Extensions are
initialized before xcore's plugin supervisor exists, so the `<remote>`/
`<action>` template tags and the cache backend are wired separately, via
`bind_engine()`, once `await xcore.boot(app)` has completed.

See docs/integration-xcore.md for the full wiring example.
"""

import secrets
from pathlib import Path
from typing import Any, Optional

from ..cache import CacheBackend
from ..core.renderer import TemplateEngine

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI = None  # type: ignore
    StaticFiles = None  # type: ignore

try:
    from xcore.services.base import BaseService, ServiceStatus
except ImportError:
    ServiceStatus = None  # type: ignore

    class BaseService:  # type: ignore
        name = "service"

        def __init__(self) -> None:
            self._status = None


class XCoreCacheBackend(CacheBackend):
    """Bridge microframe cache -> xcore's async CacheService.

    xcore's CacheService is async-only (`await cache.get(key)`, etc.). Rather
    than faking sync behavior with `asyncio.run()` (which deadlocks once
    called from inside the running loop that TemplateEngine.render() already
    executes in), these methods just return the coroutine straight through.
    TemplateEngine awaits it for you via `_maybe_await` — see renderer.py.
    """

    def __init__(self, cache_service: Any):
        self._cache = cache_service

    def get(self, key: str, ttl: Optional[int] = None):
        return self._cache.get(key)

    def set(self, key: str, value: Any):
        return self._cache.set(key, value)

    def delete(self, key: str):
        return self._cache.delete(key)

    def clear(self):
        return self._cache.clear()


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


class TemplateEngineExtension(BaseService):
    """xcore extension wrapping a MicroFrame TemplateEngine.

    Declare in xcore.yaml:

        services:
          extensions:
            template_engine:
              module: microframe.engine.integration.xcore:TemplateEngineExtension
              config:
                directory: templates
                enable_ui: true

    Access from a plugin:
        engine = self.get_service("ext.template_engine").engine
        html = await engine.render("page.html", payload)
    """

    name = "template_engine"

    def __init__(self, config: Optional[dict] = None):
        super().__init__()
        self._config = config or {}
        self.engine: Optional[TemplateEngine] = None

    async def init(self) -> None:
        self.engine = TemplateEngine(**self._config)
        if ServiceStatus is not None:
            self._status = ServiceStatus.READY

    async def shutdown(self) -> None:
        if ServiceStatus is not None:
            self._status = ServiceStatus.STOPPED

    async def health_check(self) -> tuple:
        return (self.engine is not None, "engine ready" if self.engine else "not initialized")

    def status(self) -> dict:
        return {
            "name": self.name,
            "status": self._status.value if self._status is not None else "unknown",
        }


def bind_engine(xcore_instance: Any, engine: TemplateEngine, static_prefix: str = "/static") -> dict:
    """Wire an already-built TemplateEngine to a booted xcore instance.

    Must be called AFTER `await xcore.boot(app)`, since xcore's services
    and plugin supervisor don't exist until boot() completes. Wires:
      - cache -> xcore's CacheService, if registered
      - <remote>/<action> tags -> xcore.plugins.call(), resolved lazily
        at render time (so plugin hot-reloads are picked up)
      - static() -> XCoreStatic with the given mount prefix

    Returns the per-instance action-token map, needed by
    `register_action_routes()`.
    """
    services = getattr(xcore_instance, "services", None)
    if services is not None and services.has("cache"):
        engine.set_cache_backend(XCoreCacheBackend(services.get("cache")))

    async def _remote_caller(name: str, kwargs: dict) -> Optional[str]:
        try:
            plugin, action = name.split(".", 1)
        except ValueError:
            return None
        try:
            result = await xcore_instance.plugins.call(plugin, action, kwargs)
        except Exception:
            return None
        if isinstance(result, dict):
            return result.get("html") or result.get("result") or str(result)
        return str(result) if result else None

    action_map: dict = {}

    def _action_resolver(name: str, kwargs: dict) -> str:
        try:
            plugin, action = name.split(".", 1)
        except ValueError:
            return "#"
        token = secrets.token_hex(16)
        action_map[token] = (plugin, action)
        return f"/_/a/{token}"

    engine.env.globals["_remote_caller"] = _remote_caller
    engine.env.globals["_action_resolver"] = _action_resolver

    static_helper = XCoreStatic(mount_prefix=static_prefix, asset_versions=engine._asset_versions)
    engine.add_global("static", static_helper)

    return action_map


def register_action_routes(
    app: "FastAPI",
    xcore_instance: Any,
    engine: TemplateEngine,
    action_map: dict,
    prefix: str = "/_/a",
):
    """Register the opaque action handler on a FastAPI app.

    Routes POST /_/a/<token> -> resolves the (plugin, action) pair created
    by bind_engine()'s action resolver -> validates CSRF -> calls the
    plugin via xcore.plugins.call() (caller=None: direct HTTP call,
    tenant_id read from request.state.tenant_id as set by xcore's
    TenantMiddleware) -> redirects or returns HTML.
    """
    if not FastAPI:
        raise ImportError("fastapi is required for register_action_routes()")

    from fastapi import Request
    from fastapi.responses import HTMLResponse, RedirectResponse

    @app.post(prefix + "/{token}")
    async def handle_action(token: str, request: Request):
        entry = action_map.get(token)
        if not entry:
            return HTMLResponse("<!-- invalid action -->", status_code=404)

        plugin, action = entry
        form = await request.form()
        form_data = dict(form)

        csrf_token = form_data.pop("csrf_token", "")
        redirect = form_data.pop("redirect", "")

        if csrf_token != engine.csrf_token:
            return HTMLResponse("<!-- csrf invalid -->", status_code=403)

        tenant_id = getattr(request.state, "tenant_id", "default")
        result = await xcore_instance.plugins.call(plugin, action, form_data, tenant_id=tenant_id)
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
        raise ImportError("fastapi is required for mount_template_static()")

    static_path = Path(template_dir) / "static"
    if static_path.is_dir():
        app.mount(url_prefix, StaticFiles(directory=str(static_path)), name=name)
