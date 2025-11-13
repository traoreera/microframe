# microframework/routing.py
"""
Système de routing avec APIRouter pour organiser les routes en modules
"""
import inspect
from typing import Any, Callable, Dict, List

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .dependencies import DependencyManager, RequestValidator


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


class APIRouter:
    """
    Router pour organiser les routes en modules

    Exemple:
        router = APIRouter(prefix="/api/v1", tags=["API"])

        @router.get("/users")
        async def get_users():
            return {"users": []}

        app.include_router(router)
    """

    def __init__(
        self,
        prefix: str = "",
        tags: List[str] = None,
        dependencies: List[Any] = None,
        responses: Dict[int, Dict] = None,
        deprecated: bool = False,
        include_in_schema: bool = True,
    ):
        self.prefix = prefix.rstrip("/")  # Enlever le / final
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.responses = responses or {}
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema

        self._routes: List[RouteInfo] = []
        self._dependency_manager = DependencyManager()

    def add_route(self, path: str, func: Callable, methods: List[str] = None, **kwargs):
        """Ajoute une route au router"""
        if methods is None:
            methods = ["GET"]

        # Combiner le préfixe avec le path
        full_path = f"{self.prefix}{path}"

        # Combiner les tags
        route_tags = kwargs.get("tags", [])
        all_tags = list(set(self.tags + route_tags))

        # Créer l'info de route
        route_info = RouteInfo(
            path=full_path,
            func=func,
            methods=methods,
            tags=all_tags,
            summary=kwargs.get("summary"),
            description=kwargs.get("description"),
            response_model=kwargs.get("response_model"),
            status_code=kwargs.get("status_code", 200),
            deprecated=kwargs.get("deprecated", self.deprecated),
            include_in_schema=kwargs.get("include_in_schema", self.include_in_schema),
        )

        self._routes.append(route_info)

        return func

    def get(self, path: str, **kwargs):
        """Décorateur pour route GET"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["GET"], **kwargs)

        return decorator

    def post(self, path: str, **kwargs):
        """Décorateur pour route POST"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["POST"], **kwargs)

        return decorator

    def put(self, path: str, **kwargs):
        """Décorateur pour route PUT"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["PUT"], **kwargs)

        return decorator

    def patch(self, path: str, **kwargs):
        """Décorateur pour route PATCH"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["PATCH"], **kwargs)

        return decorator

    def delete(self, path: str, **kwargs):
        """Décorateur pour route DELETE"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["DELETE"], **kwargs)

        return decorator

    def options(self, path: str, **kwargs):
        """Décorateur pour route OPTIONS"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["OPTIONS"], **kwargs)

        return decorator

    def head(self, path: str, **kwargs):
        """Décorateur pour route HEAD"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=["HEAD"], **kwargs)

        return decorator

    def route(self, path: str, methods: List[str] = None, **kwargs):
        """Décorateur générique pour route"""

        def decorator(func: Callable):
            return self.add_route(path, func, methods=methods, **kwargs)

        return decorator

    def include_router(
        self,
        router: "APIRouter",
        prefix: str = "",
        tags: List[str] = None,
        dependencies: List[Any] = None,
    ):
        """
        Inclut un autre router dans ce router

        Exemple:
            users_router = APIRouter()
            api_router = APIRouter(prefix="/api")
            api_router.include_router(users_router, prefix="/users")
        """
        # Combiner les préfixes
        combined_prefix = f"{self.prefix}{prefix}".rstrip("/")

        # Combiner les tags
        combined_tags = list(set(self.tags + (tags or [])))

        # Copier les routes avec le nouveau préfixe
        for route_info in router._routes:
            # Retirer le préfixe original du router inclus
            path_without_prefix = route_info.path
            if router.prefix:
                path_without_prefix = route_info.path[len(router.prefix) :]

            # Créer une nouvelle route avec le préfixe combiné
            new_route = RouteInfo(
                path=f"{combined_prefix}{path_without_prefix}",
                func=route_info.func,
                methods=route_info.methods,
                tags=list(set(combined_tags + route_info.tags)),
                summary=route_info.summary,
                description=route_info.description,
                response_model=route_info.response_model,
                status_code=route_info.status_code,
                deprecated=route_info.deprecated,
                include_in_schema=route_info.include_in_schema,
            )

            self._routes.append(new_route)

    def get_routes(self) -> List[RouteInfo]:
        """Retourne toutes les routes du router"""
        return self._routes.copy()


def build_route_handler(route_info: RouteInfo, dependency_manager: DependencyManager):
    """
    Construit un handler Starlette à partir d'une RouteInfo
    """

    async def endpoint(request: Request):
        try:
            # Validation des paramètres
            params = await RequestValidator.parse_request(request, route_info.func)

            # Résolution des dépendances
            deps = await dependency_manager.resolve(route_info.func, request)

            # Exécution de la fonction
            if inspect.iscoroutinefunction(route_info.func):
                result = await route_info.func(**params, **deps)
            else:
                result = route_info.func(**params, **deps)

            # Retour de la réponse
            if isinstance(result, JSONResponse):
                return result

            return JSONResponse(result, status_code=route_info.status_code)

        except Exception:
            # Les exceptions sont gérées par l'application
            raise

    return endpoint
