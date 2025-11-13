"""
Optimized dependency injection manager
"""

import inspect
import logging
from typing import Any, Callable, Dict, Optional, get_type_hints

from starlette.requests import Request

from ..core.exceptions import DependencyException
from .exceptionHandler import Depends

logger = logging.getLogger(__name__)


class DependencyManager:
    """
    Advanced dependency injection manager

    Features:
    - Named dependencies
    - Depends() style dependencies
    - Caching support
    - Circular dependency detection
    - Async/sync function support
    """

    def __init__(self):
        self._dependencies: Dict[str, Callable] = {}
        self._cache: Dict[str, Any] = {}
        self._resolving: set = set()

    def register(self, name: str, func: Callable, cache: bool = False):
        """Register a named dependency"""
        self._dependencies[name] = func
        if cache:
            self._cache[name] = None

    async def resolve(self, func: Callable, request: Optional[Request] = None) -> Dict[str, Any]:
        """
        Resolve all dependencies for a function

        Args:
            func: Function to resolve dependencies for
            request: Optional request object

        Returns:
            Dictionary of resolved dependencies
        """
        resolved = {}
        sig = inspect.signature(func)

        try:
            get_type_hints(func)
        except Exception:
            pass

        for param_name, param in sig.parameters.items():
            # Skip request and self
            if param_name in ["request", "self"]:
                continue

            # Case 1: Explicit Depends()
            if isinstance(param.default, Depends):
                resolved[param_name] = await self._resolve_depends(param.default, request)

            # Case 2: Named dependency
            elif param_name in self._dependencies:
                resolved[param_name] = await self._resolve_named(param_name, request)

        return resolved

    async def _resolve_depends(self, depends: Depends, request: Optional[Request]) -> Any:
        """Resolve a Depends() dependency"""
        cache_key = depends._cache_key

        # Check cache
        if depends.use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        # Check circular dependencies
        dep_id = id(depends.dependency)
        if dep_id in self._resolving:
            raise DependencyException(
                f"Circular dependency detected: {depends.dependency.__name__}"
            )

        self._resolving.add(dep_id)

        try:
            # Resolve sub-dependencies
            sub_deps = await self.resolve(depends.dependency, request)

            # Add request if needed
            sig = inspect.signature(depends.dependency)
            if "request" in sig.parameters and request is not None:
                sub_deps["request"] = request

            # Call dependency
            result = await self._call(depends.dependency, **sub_deps)

            # Cache if enabled
            if depends.use_cache:
                self._cache[cache_key] = result

            return result

        finally:
            self._resolving.discard(dep_id)

    async def _resolve_named(self, name: str, request: Optional[Request]) -> Any:
        """Resolve a named dependency"""
        # Check cache
        if name in self._cache and self._cache[name] is not None:
            return self._cache[name]

        dep_func = self._dependencies[name]

        # Resolve sub-dependencies
        sub_deps = await self.resolve(dep_func, request)

        # Add request if needed
        sig = inspect.signature(dep_func)
        if "request" in sig.parameters and request is not None:
            sub_deps["request"] = request

        # Call dependency
        result = await self._call(dep_func, **sub_deps)

        # Cache if configured
        if name in self._cache:
            self._cache[name] = result

        return result

    async def _call(self, func: Callable, **kwargs) -> Any:
        """Call a function (sync or async)"""
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)

    def clear_cache(self):
        """Clear dependency cache"""
        self._cache.clear()
