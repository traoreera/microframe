"""
Router for organizing routes - VERSION FINALE CORRIGÉE
"""

from typing import Any, Callable, List, Optional


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

    def __repr__(self):
        return f"RouteInfo(path={self.path}, methods={self.methods}, tags={self.tags})"


class Router:
    """
    Router for organizing routes into modules

    Architecture:
    - Les routes sont stockées avec leur path RELATIF (sans prefix)
    - Les routers imbriqués sont stockés séparément avec leur prefix
    - get_routes() reconstruit tous les paths en combinant les préfixes

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
        # Normaliser le prefix (retirer le / final)
        self.prefix = prefix.rstrip("/") if prefix else ""
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema

        # Stockage des routes locales (avec paths RELATIFS)
        self._routes: List[RouteInfo] = []

        # Stockage des routers imbriqués: (router, prefix_additionnel, tags_additionnels)
        self._nested_routers: List[tuple[Router, str, List[str]]] = []

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
        """
        Add a route to the router

        Le path est stocké RELATIF (sans le prefix du router)
        """
        if methods is None:
            methods = ["GET"]

        # Normaliser le path (s'assurer qu'il commence par /)
        if not path.startswith("/"):
            path = f"/{path}"

        # Merge tags (tags du router + tags de la route)
        route_tags = tags or []
        all_tags = list(set(self.tags + route_tags))

        # ✅ Créer RouteInfo avec path RELATIF
        route_info = RouteInfo(
            path=path,  # Path relatif uniquement
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
        Include another router into this router

        Args:
            router: Router instance to include
            prefix: Additional prefix to prepend to all routes
            tags: Additional tags to add to all routes

        Example:
            main_router = Router(prefix="/api")
            users_router = Router(prefix="/users", tags=["Users"])

            @users_router.get("/")
            def list_users(): pass

            main_router.include_router(users_router, prefix="/v1", tags=["V1"])
            # Result: /api/v1/users/ with tags ["Users", "V1"]
        """
        if not isinstance(router, Router):
            raise TypeError(f"Expected Router instance, got {type(router).__name__}")

        # Normaliser le prefix additionnel
        additional_prefix = prefix.rstrip("/") if prefix else ""
        additional_tags = tags or []

        # ✅ Stocker le router imbriqué au lieu de copier ses routes
        self._nested_routers.append((router, additional_prefix, additional_tags))

    def get_routes(self, prefix: str = "", tags: Optional[List[str]] = None) -> List[RouteInfo]:
        """
        Get all routes with complete paths

        Reconstruit récursivement tous les paths en combinant:
        - prefix externe (de l'Application)
        - prefix du router actuel
        - prefix additionnel (de include_router)
        - prefix des routers imbriqués
        - path de la route

        Args:
            prefix: Prefix externe (généralement de l'Application)
            tags: Tags externes (généralement de l'Application)

        Returns:
            List of RouteInfo with complete paths
        """
        all_routes = []
        additional_tags = tags or []

        # ✅ Traiter les routes locales
        for route_info in self._routes:
            # Construire le path complet: prefix_externe + prefix_router + path_route
            full_path = f"{prefix}{self.prefix}{route_info.path}"

            # Normaliser (éviter //)
            full_path = full_path.replace("//", "/")

            # Combiner les tags
            combined_tags = list(set(route_info.tags + additional_tags))

            complete_route = RouteInfo(
                path=full_path,
                func=route_info.func,
                methods=route_info.methods,
                tags=combined_tags,
                summary=route_info.summary,
                description=route_info.description,
                response_model=route_info.response_model,
                status_code=route_info.status_code,
                deprecated=route_info.deprecated,
                include_in_schema=route_info.include_in_schema,
            )
            all_routes.append(complete_route)

        # ✅ Traiter les routers imbriqués (récursion)
        for nested_router, nested_prefix, nested_tags in self._nested_routers:
            # Combiner le prefix: prefix_externe + prefix_router + prefix_additionnel
            combined_prefix = f"{prefix}{self.prefix}{nested_prefix}"

            # Combiner les tags
            combined_tags = list(set(additional_tags + nested_tags))

            # Récupérer les routes du router imbriqué (récursion)
            nested_routes = nested_router.get_routes(prefix=combined_prefix, tags=combined_tags)

            all_routes.extend(nested_routes)

        return all_routes

    def __repr__(self):
        return f"Router(prefix='{self.prefix}', routes={len(self._routes)}, nested={len(self._nested_routers)}, tags={self.tags})"
