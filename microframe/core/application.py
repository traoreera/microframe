# microframework/app.py
import inspect
import logging
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, ValidationError
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
)
from starlette.routing import Route

from microframe.dependencies import AppException, DependencyManager
from microframe.docs import OpenAPIGenerator, ReDocUI, SwaggerUI
from microframe.routing.router import RouteInfo, Router
from microframe.validation import RequestParser

from .config import AppConfig


class Application(Starlette):
    """Application principale (framework unifié et extensible)"""

    def __init__(self, configuration: AppConfig = AppConfig()):
        # --- META ---
        self.config = configuration

        # --- COMPOSANTS PRINCIPAUX ---
        self._routes_info: List[RouteInfo] = []
        self._dependency_manager = DependencyManager()
        self._routers: List[Router] = []

        # --- LOGGING ---
        logging.basicConfig(
            level=logging.DEBUG if self.config.debug else logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(self.config.title)

        # --- INIT STARLETTE ---
        super().__init__(
            routes=[],
            middleware=self.config.middleware or [],
            exception_handlers={
                AppException: self._app_exception_handler,
                ValidationError: self._validation_exception_handler,
                Exception: self._global_exception_handler,
            },
        )

        # --- ROUTES INTERNES (DOCS + OPENAPI) ---
        if self.config.docs_url or self.config.redoc_url:
            self._register_internal_routes()

        self.logger.info(
            f"✅ Application '{self.config.title}' initialisée (v{self.config.version})"
        )

    # ============================================================
    # === DÉCORATEURS ROUTES =====================================
    # ============================================================

    def route(
        self,
        path: str,
        methods: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_model: Any = None,
        status_code: int = 200,
        deprecated: bool = False,
        include_in_schema: bool = True,
    ):
        """Décorateur pour enregistrer une route"""
        if methods is None:
            methods = ["GET"]
        if tags is None:
            tags = []

        def decorator(func: Callable):
            route_info = RouteInfo(
                path=path,
                func=func,
                methods=methods,
                tags=tags,
                summary=summary,
                description=description,
                response_model=response_model,
                status_code=status_code,
                deprecated=deprecated,
                include_in_schema=include_in_schema,
            )

            route = self._build_route(route_info)
            self._add_route(route_info, route)
            self.logger.debug(f"📡 Route enregistrée: {methods} {path}")
            return func

        return decorator

    def get(self, path: str, **kwargs):
        return self.route(path, methods=["GET"], **kwargs)

    def post(self, path: str, **kwargs):
        return self.route(path, methods=["POST"], **kwargs)

    def put(self, path: str, **kwargs):
        return self.route(path, methods=["PUT"], **kwargs)

    def patch(self, path: str, **kwargs):
        return self.route(path, methods=["PATCH"], **kwargs)

    def delete(self, path: str, **kwargs):
        return self.route(path, methods=["DELETE"], **kwargs)

    # ============================================================
    # === DÉPENDANCES ============================================
    # ============================================================

    def dependency(
        self,
        name: str = "",
        cache: bool = False,
        scope: Literal["app", "request"] = "request",
    ):
        """Décorateur pour enregistrer une dépendance"""

        def decorator(func: Callable):
            dep_name = name or func.__name__
            self._dependency_manager.register(dep_name, func, cache)
            self.logger.debug(f"🔗 Dépendance enregistrée: {dep_name} (scope={scope})")
            return func

        return decorator

    # ============================================================
    # === ROUTERS ================================================
    # ============================================================

    def include_router(
        self,
        router: Router,
        prefix: str = "",
        tags: Optional[List[str]] = None,
    ):
        """Inclut un Router complet"""
        if not hasattr(router, "get_routes"):
            raise ValueError("Objet fourni non valide: doit être un Router")

        combined_prefix = prefix.rstrip("/")
        router_routes = router.get_routes()
        self._routers.append(router)

        self.logger.info(
            f"🧩 Inclusion router: {len(router_routes)} routes (prefix='{combined_prefix or '/'}')"
        )

        for r in router_routes:
            full_path = f"{combined_prefix}{r.path}"
            all_tags = list(set((tags or []) + r.tags))

            route_info = RouteInfo(
                path=full_path,
                func=r.func,
                methods=r.methods,
                tags=all_tags,
                summary=r.summary,
                description=r.description,
                response_model=r.response_model,
                status_code=r.status_code,
                deprecated=r.deprecated,
                include_in_schema=r.include_in_schema,
            )
            route = self._build_route(route_info)
            self._add_route(route_info, route)

        self.logger.info(f"✅ Router inclus: {len(router_routes)} routes ajoutées")

    # ============================================================
    # === ROUTES MANAGEMENT ======================================
    # ============================================================

    def _add_route(self, info: RouteInfo, route: Route):
        """Ajoute une route dans Starlette et le registre interne"""
        self.routes.append(route)
        self._routes_info.append(info)

    def _build_route(self, info: RouteInfo) -> Route:
        """Construit une route Starlette"""

        async def endpoint(request: Request):
            try:
                # Parse request parameters (body, query, path)
                params = await RequestParser().parse(request, info.func)

                # Add path parameters from Starlette
                path_params = dict(request.path_params)

                # Resolve dependencies
                deps = await self._dependency_manager.resolve(info.func, request)

                # Merge all kwargs (path params override query params)
                all_kwargs = {**params, **path_params, **deps}

                # Call the endpoint function
                result = await self._call_endpoint(info.func, all_kwargs)

                # Handle different response types
                if isinstance(
                    result,
                    (
                        JSONResponse,
                        HTMLResponse,
                        FileResponse,
                        RedirectResponse,
                        StreamingResponse,
                        PlainTextResponse,
                        Response,
                    ),
                ):
                    return result
                # pydantic models
                if isinstance(result, dict):
                    return JSONResponse(result, status_code=info.status_code)
                # Default: return JSON
                return JSONResponse(result.model_dump(), status_code=info.status_code)

            except AppException as e:
                return await self._app_exception_handler(request, e)
            except ValidationError as e:
                return await self._validation_exception_handler(request, e)
            except Exception as e:
                return await self._global_exception_handler(request, e)

        return Route(info.path, endpoint=endpoint, methods=info.methods)

    async def _call_endpoint(self, func: Callable, kwargs: Dict):
        """Exécute un endpoint (sync/async)"""
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)

    # ============================================================
    # === GESTION DES EXCEPTIONS ================================
    # ============================================================

    async def _app_exception_handler(self, request: Request, exc: AppException):
        """Gère les exceptions métier de l'application"""
        return JSONResponse(
            {"error": exc.message, "details": exc.details}, status_code=exc.status_code
        )

    async def _validation_exception_handler(self, request: Request, exc: ValidationError):
        """Gère les erreurs de validation Pydantic"""
        return JSONResponse({"error": "Validation error", "details": exc.errors()}, status_code=422)

    async def _global_exception_handler(self, request: Request, exc: Exception):

        if isinstance(exc, HTTPException):
            return JSONResponse(
                {"error": exc.detail, "details": exc.headers}, status_code=exc.status_code
            )

        return JSONResponse(
            {"error": "Internal server error", "details": str(exc)}, status_code=500
        )

    # ============================================================
    # === DOCS & OPENAPI ========================================
    # ============================================================

    def _register_internal_routes(self):
        """Définit les routes internes (/docs, /openapi.json, /redoc)"""

        async def openapi(request: Request):
            openapi_gen = OpenAPIGenerator(
                routes=self._routes_info,
                title=self.config.title,
                version=self.config.version,
                description=self.config.description,
            )
            return JSONResponse(openapi_gen.generate())

        async def docs(request: Request):
            return SwaggerUI(title=self.config.title)()

        async def redoc(request: Request):
            return ReDocUI(title=self.config.title)()

        internal_routes = [
            Route(self.config.openapi_url, endpoint=openapi, methods=["GET"]),
        ]

        # Ajouter docs si configuré
        if self.config.docs_url:
            docs_path = (
                self.config.docs_url
                if self.config.docs_url.startswith("/")
                else f"/{self.config.docs_url}"
            )
            internal_routes.append(Route(docs_path, endpoint=docs, methods=["GET"]))

        # Ajouter redoc si configuré
        if self.config.redoc_url:
            redoc_path = (
                self.config.redoc_url
                if self.config.redoc_url.startswith("/")
                else f"/{self.config.redoc_url}"
            )
            internal_routes.append(Route(redoc_path, endpoint=redoc, methods=["GET"]))

        self.routes.extend(internal_routes)
        self.logger.debug("📚 Routes internes (docs/openapi/redoc) enregistrées")

    def _extract_schema(self, func: Callable):
        """Extrait le schéma OpenAPI d'une fonction"""
        sig = inspect.signature(func)
        params = []
        request_body = None

        for name, param in sig.parameters.items():
            # Ignorer les paramètres spéciaux
            if name in ["self", "cls", "request", "db"]:
                continue

            ann = param.annotation

            # Gestion des modèles Pydantic
            if RequestParser()._is_pydantic_model(ann):
                schema = ann.model_json_schema()
                request_body = {
                    "required": True,
                    "content": {"application/json": {"schema": schema}},
                }
            else:
                # Déterminer le type de paramètre
                param_type = "string"
                if ann == int:
                    param_type = "integer"
                elif ann == float:
                    param_type = "number"
                elif ann == bool:
                    param_type = "boolean"

                # Paramètres de query/path
                params.append(
                    {
                        "name": name,
                        "in": "query",  # Sera changé en "path" par OpenAPIGenerator si nécessaire
                        "required": param.default == inspect.Parameter.empty,
                        "schema": {"type": param_type},
                    }
                )

        return params, request_body
