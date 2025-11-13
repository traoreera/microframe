"""
Router for organizing routes - VERSION CORRIGÉE
"""

from typing import Any, Callable, List, Optional

from ..validation.parser import RequestParser


class RouteInfo:
    """Information sur une route"""

    def __init__(
        self,
        path: str,
        func: Callable,
        methods: List[str],
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_model: Any = None,
        status_code: int = 200,
        deprecated: bool = False,
        include_in_schema: bool = True,
    ):
        self.path = path
        self.func = func
        self.methods = methods
        self.tags = tags or []
        self.summary = summary or func.__name__
        self.description = description or (func.__doc__ or "").strip()
        self.response_model = response_model
        self.status_code = status_code
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema


class Router:
    """
    Router for organizing routes into modules

    Example:
        router = Router(prefix="/api/v1", tags=["API"])

        @router.get("/users")
        async def get_users():
            return {"users": []}

        app.include_router(router)
    """

    def __init__(
        self,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[Any]] = None,
        deprecated: bool = False,
        include_in_schema: bool = True,
    ):
        self.prefix = prefix.rstrip("/")
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema
        self._routes: List[RouteInfo] = []
        self._routers: List[tuple] = []  # (router, prefix, tags)

    def add_route(
        self,
        path: str,
        func: Callable,
        methods: Optional[List[str]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_model: Any = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        deprecated: bool = False,
        include_in_schema: bool = True,
        **kwargs,
    ) -> Callable:
        """Add a route to the router"""
        if methods is None:
            methods = ["GET"]

        # Build full path
        full_path = f"{self.prefix}{path}"

        # Merge tags
        route_tags = tags or []
        all_tags = list(set(self.tags + route_tags))

        # Create route info
        route_info = RouteInfo(
            path=full_path,
            func=func,
            methods=methods,
            tags=all_tags,
            summary=summary or func.__name__,
            description=description or (func.__doc__ or "").strip(),
            response_model=response_model,
            status_code=status_code,
            deprecated=deprecated or self.deprecated,
            include_in_schema=include_in_schema and self.include_in_schema,
        )

        self._routes.append(route_info)
        return func

    def get(self, path: str, **kwargs) -> Callable:
        """GET route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["GET"], **kwargs)

        return decorator

    def post(self, path: str, **kwargs) -> Callable:
        """POST route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["POST"], **kwargs)

        return decorator

    def put(self, path: str, **kwargs) -> Callable:
        """PUT route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["PUT"], **kwargs)

        return decorator

    def patch(self, path: str, **kwargs) -> Callable:
        """PATCH route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["PATCH"], **kwargs)

        return decorator

    def delete(self, path: str, **kwargs) -> Callable:
        """DELETE route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["DELETE"], **kwargs)

        return decorator

    def options(self, path: str, **kwargs) -> Callable:
        """OPTIONS route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["OPTIONS"], **kwargs)

        return decorator

    def head(self, path: str, **kwargs) -> Callable:
        """HEAD route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=["HEAD"], **kwargs)

        return decorator

    def route(self, path: str, methods: Optional[List[str]] = None, **kwargs) -> Callable:
        """Generic route decorator"""

        def decorator(func: Callable) -> Callable:
            return self.add_route(path, func, methods=methods, **kwargs)

        return decorator

    def include_router(self, router: "Router", prefix: str = "", tags: Optional[List[str]] = None):
        """
        Include another router

        Args:
            router: Router to include
            prefix: Additional prefix for routes
            tags: Additional tags
        """
        self._routers.append((router, prefix, tags or []))

    def get_routes(self, prefix: str = "", tags: Optional[List[str]] = None) -> List[RouteInfo]:
        """
        Get all routes including nested routers

        Args:
            prefix: Additional prefix to prepend
            tags: Additional tags to add

        Returns:
            List of all route info objects
        """
        all_routes = []
        additional_tags = tags or []

        # Process direct routes
        for route_info in self._routes:
            # Clone route info with updated path and tags
            updated_route = RouteInfo(
                path=f"{prefix}{route_info.path}",
                func=route_info.func,
                methods=route_info.methods,
                tags=list(set(route_info.tags + additional_tags)),
                summary=route_info.summary,
                description=route_info.description,
                response_model=route_info.response_model,
                status_code=route_info.status_code,
                deprecated=route_info.deprecated,
                include_in_schema=route_info.include_in_schema,
            )
            all_routes.append(updated_route)

        # Process nested routers
        for nested_router, nested_prefix, nested_tags in self._routers:
            combined_prefix = f"{prefix}{nested_prefix}"
            combined_tags = list(set(additional_tags + nested_tags))

            nested_routes = nested_router.get_routes(prefix=combined_prefix, tags=combined_tags)
            all_routes.extend(nested_routes)

        return all_routes
