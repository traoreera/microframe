import asyncio
import hashlib
import inspect
import json
import logging
import re
import secrets
import time
from typing import Any, Callable, Dict, List, Optional

import jinja2

from ..cache import CacheBackend, CacheManager
from ..mfe import MFEClient
from .environment import build_environment

logger = logging.getLogger(__name__)


class TemplateEngine:
    _instance: Optional["TemplateEngine"] = None

    def __init__(
        self,
        directory: str = "templates",
        debug: bool = True,
        bytecode_cache: bool = False,
        enable_minify: bool = True,
        enable_cache: bool = False,
        enable_ui: bool = False,
        cache_ttl: int = 300,
        cache_backend: Optional[CacheBackend] = None,
        mfe_timeout: float = 5.0,
        remote_caller: Optional[Callable] = None,
        action_resolver: Optional[Callable] = None,
    ):
        self.directory = directory
        self.enable_minify = enable_minify
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self._cache = cache_backend or CacheManager()
        self._asset_versions: Dict[str, str] = {}
        self._csrf_token = secrets.token_urlsafe(32)
        self.mfe = MFEClient(timeout=mfe_timeout)

        self._context_processors: List[Callable] = []

        self.env = build_environment(
            directory=directory,
            debug=debug,
            bytecode_cache=bytecode_cache,
            mfe_client=self.mfe,
            asset_versions=self._asset_versions,
            enable_ui=enable_ui,
            remote_caller=remote_caller,
            action_resolver=action_resolver,
            csrf_token=self._csrf_token,
        )

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    async def render(
        self,
        template_name: str,
        ctx: Optional[Dict[str, Any]] = None,
        use_cache: Optional[bool] = None,
    ) -> str:
        """Render a template and return the HTML string."""
        ctx = dict(ctx or {})

        for processor in self._context_processors:
            sig = inspect.signature(processor)
            params = list(sig.parameters.values())
            if len(params) == 1:
                result = processor(ctx)
            else:
                result = processor()
            if asyncio.iscoroutine(result):
                result = await result
            if isinstance(result, dict):
                ctx.update(result)

        cached_enabled = self.enable_cache if use_cache is None else use_cache

        if cached_enabled:
            key = self._cache_key(template_name, ctx)
            hit = self._cache.get(key, self.cache_ttl)
            if hit:
                logger.debug(f"Cache hit: {template_name}")
                return hit

        try:
            start = time.time()
            template = self.env.get_template(template_name)
            html = await template.render_async(**ctx)
            html = self._minify(html)

            if cached_enabled:
                self._cache.set(key, html)

            logger.debug(f"Rendered {template_name} in {(time.time() - start) * 1000:.2f}ms")
            return html

        except jinja2.TemplateNotFound:
            logger.error(f"Template not found: {template_name}")
            return f"<h1>Template Error</h1><p>'{template_name}' not found</p>"
        except Exception as e:
            logger.exception(f"Error rendering '{template_name}'")
            return f"<h1>Render Error</h1><pre>{type(e).__name__}: {e}</pre>"

    # ------------------------------------------------------------------
    # Customization
    # ------------------------------------------------------------------

    def add_context_processor(self, func: Callable):
        self._context_processors.append(func)

    def add_global(self, name: str, value: Any):
        self.env.globals[name] = value

    def add_filter(self, name: str, func: Callable):
        self.env.filters[name] = func

    def set_asset_version(self, path: str, version: str):
        self._asset_versions[path] = version

    def list_templates(self):
        return self.env.list_templates()

    def clear_cache(self):
        self._cache.clear()
        logger.info("Template cache cleared")

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _cache_key(self, template_name: str, ctx: dict) -> str:
        raw = json.dumps(ctx, sort_keys=True, default=str)
        return hashlib.sha224(f"{template_name}:{raw}".encode()).hexdigest()

    def _minify(self, html: str) -> str:
        if not self.enable_minify:
            return html
        protected: list = []

        def save(match):
            protected.append(match.group(0))
            return f"___P{len(protected) - 1}___"

        html = re.sub(r"<(pre|textarea|script)[\s\S]*?</\1>", save, html, flags=re.IGNORECASE)
        html = re.sub(r"<!--(?!\[if).*?-->", "", html, flags=re.DOTALL)
        html = re.sub(r"[ \t]+", " ", html)
        html = re.sub(r">\s+<", "><", html)
        html = re.sub(r"\n\s*\n", "\n", html)

        for i, block in enumerate(protected):
            html = html.replace(f"___P{i}___", block)

        return html.strip()

    # ------------------------------------------------------------------
    # Singleton
    # ------------------------------------------------------------------

    @classmethod
    def instance(cls, **kwargs) -> "TemplateEngine":
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        cls._instance = None
