# microframework/app.py
import inspect
import logging
from typing import Any, Dict, List, Callable, Optional, Literal
from pydantic import ValidationError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware import Middleware

from .dependencies import AppException, RequestValidator, DependencyManager
from .routing import RouteInfo, Router as APIRouter
from .docs.ui import ReDocUI, SwaggerUI
from .docs.openapi import OpenAPIGenerator



class Application(Starlette):
    """Application principale (framework unifié et extensible)"""

    def __init__(
        self,
        title: str = "MicroFramework",
        version: str = "1.0.0",
        description: str = "",
        middleware: Optional[List[Middleware]] = None,
        debug: bool = False,
    ):
        # --- META ---
        self.title = title
        self.version = version
        self.description = description
        self.debug = debug

        # --- COMPOSANTS PRINCIPAUX ---
        self._routes_info: List[RouteInfo] = []
        self._dependency_manager = DependencyManager()
        self._routers: List[Dict[str, Any]] = []


        # --- LOGGING ---
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(self.title)

        # --- INIT STARLETTE ---
        super().__init__(
            routes=[],
            middleware=middleware or [],
            exception_handlers={
                AppException: self._app_exception_handler,
                ValidationError: self._validation_exception_handler,
                Exception: self._generic_exception_handler,
            },
        )

        # --- ROUTES INTERNES (DOCS + OPENAPI) ---
        self._register_internal_routes()

        self.logger.info(f"✅ Application '{self.title}' initialisée (v{self.version})")

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
            self._dependency_manager.register(dep_name, func, cache, scope)
            self.logger.debug(f"🔗 Dépendance enregistrée: {dep_name} (scope={scope})")
            return func

        return decorator

    # ============================================================
    # === ROUTERS ================================================
    # ============================================================

    def include_router(
        self,
        router: APIRouter,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[Any]] = None,
    ):
        """Inclut un APIRouter complet"""
        if not hasattr(router, "get_routes"):
            raise ValueError("Objet fourni non valide: doit être un APIRouter")

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
                params = await RequestValidator.parse_request(request, info.func)
                deps = await self._dependency_manager.resolve(info.func, request)
                result = await self._call_endpoint(info.func, {**params, **deps})

                if isinstance(result, (JSONResponse, HTMLResponse)):
                    return result
                return JSONResponse(result)

            except AppException as e:
                return JSONResponse({"error": e.message, "details": e.details}, status_code=e.status_code)
            except Exception as e:
                self.logger.error(f"Erreur route {info.path}: {e}", exc_info=True)
                return JSONResponse({"error": "Internal server error"}, status_code=500)

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
        return JSONResponse({"error": exc.message, "details": exc.details}, status_code=exc.status_code)

    async def _validation_exception_handler(self, request: Request, exc: ValidationError):
        return JSONResponse({"error": "Validation error", "details": exc.errors()}, status_code=422)

    async def _generic_exception_handler(self, request: Request, exc: Exception):
        self.logger.error(f"Erreur non gérée: {exc}", exc_info=True)
        return JSONResponse({"error": "Internal server error"}, status_code=500)

    # ============================================================
    # === DOCS & OPENAPI ========================================
    # ============================================================

    def _register_internal_routes(self):
        """Définit les routes internes (/docs, /openapi.json, /redoc)"""
        async def openapi(request: Request):
            openapi = OpenAPIGenerator(routes=self._routes_info, title=self.title,version=self.version,description= self.description)

            return JSONResponse(openapi.generate())



        async def docs(request: Request):
            return SwaggerUI(title=self.title)()

        async def redoc(request: Request):
            return ReDocUI(title=self.title)()

        internal_routes = [
            Route("/openapi.json", endpoint=openapi, methods=["GET"]),
            Route("/docs", endpoint=docs, methods=["GET"]),
            Route("/redoc", endpoint=redoc, methods=["GET"]),
        ]
        self.routes.extend(internal_routes)
        self.logger.debug("📚 Routes internes (docs/openapi/redoc) enregistrées")

    def _generate_openapi(self) -> Dict:
        paths: Dict[str, Any] = {}

        for info in self._routes_info:
            if not info.include_in_schema:
                continue

            if info.path not in paths:
                paths[info.path] = {}

            for method in info.methods:
                params, body = self._extract_schema(info.func)
                paths[info.path][method.lower()] = {
                    "summary": info.summary,
                    "description": info.description,
                    "tags": info.tags,
                    "parameters": params,
                    "requestBody": body,
                    "responses": {
                        "200": {"description": "Successful Response"},
                        "422": {"description": "Validation Error"},
                        "500": {"description": "Internal Server Error"},
                    },
                }

        return {
            "openapi": "3.0.2",
            "info": {"title": self.title, "version": self.version, "description": self.description},
            "paths": paths,
        }

    def _extract_schema(self, func: Callable):
        sig = inspect.signature(func)
        params = []
        request_body = None

        for name, param in sig.parameters.items():
            ann = param.annotation

            if RequestValidator._is_pydantic_model(ann):
                schema = ann.model_json_schema()
                request_body = {
                    "required": True,
                    "content": {"application/json": {"schema": schema}},
                }
            elif name not in ["request"]:
                params.append({
                    "name": name,
                    "in": "query",
                    "required": param.default == inspect.Parameter.empty,
                    "schema": {"type": "string"},
                })

        return params, request_body

