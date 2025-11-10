# microframework/app.py
import inspect
import logging
from typing import Dict, List, Callable, Any
from pydantic import ValidationError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from starlette.middleware import Middleware

from .dependencies import AppException,RequestValidator
from .dependencies import DependencyManager
from .routing import  RouteInfo, Router as APIRouter

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)





class Application(Starlette):
    """Application principale améliorée"""
    
    def __init__(
        self, 
        title: str = "MicroFramework",
        version: str = "1.0.0",
        description: str = "",
        middleware: List[Middleware] = []
    ):
        # Initialisation des composants
        self.title = title
        self.version = version
        self.description = description
        self._routes_info: List = []
        self._dependency_manager = DependencyManager()
        self._routers = []  # Liste des routers inclus
        
        # Initialisation Starlette avec middleware
        super().__init__(
            routes=[],
            middleware=middleware or [],
            exception_handlers={
                AppException: self._app_exception_handler,
                ValidationError: self._validation_exception_handler,
                Exception: self._generic_exception_handler
            } # pyright: ignore[reportArgumentType]
        )
        
        # Enregistrement des routes de documentation
        self._register_docs()
        
        logger.info(f"Application '{title}' initialisée")
    
    def route(
        self, 
        path: str, 
        methods: List[str] = [], 
        tags: List[str] = []
    ):
        """Décorateur pour enregistrer une route"""
        if methods is None:
            methods = ["GET"]
        
        def decorator(func: Callable):
            route = self._build_route(path, func, methods, tags)
            self.routes.append(route)
            logger.info(f"Route enregistrée: {methods} {path}")
            return func
        
        return decorator
    
    def dependency(self, name: str, cache: bool = False):
        """Décorateur pour enregistrer une dépendance"""
        def decorator(func: Callable):
            dep_name = name or func.__name__
            self._dependency_manager.register(dep_name, func, cache)
            return func
        return decorator
    
    def include_router(
        self,
        router: 'APIRouter',
        prefix: str = "",
        tags: List[str] = [],
        dependencies: List[Any] = []
    ):
        """
        Inclut un APIRouter dans l'application
        
        Exemple:
            users_router = APIRouter(prefix="/users", tags=["Users"])
            
            @users_router.get("/")
            async def list_users():
                return {"users": []}
            
            app.include_router(users_router)
        """
        if APIRouter is None or not isinstance(router, type(router)):
            raise ValueError("APIRouter must be imported from microframework.routing")
        
        # Combiner les préfixes
        combined_prefix = prefix.rstrip("/")
        
        # Combiner les tags
        combined_tags = tags or []
        
        # Ajouter toutes les routes du router
        for route_info in router.get_routes():
            # Ajuster le path avec le préfixe
            full_path = route_info.path
            if combined_prefix:
                # Retirer le préfixe du router si présent
                if router.prefix and route_info.path.startswith(router.prefix):
                    path_without_router_prefix = route_info.path[len(router.prefix):]
                else:
                    path_without_router_prefix = route_info.path
                
                full_path = f"{combined_prefix}{path_without_router_prefix}"
            
            # Combiner les tags
            all_tags = list(set(combined_tags + route_info.tags))
            route_info.tags = all_tags
            route_info.path = full_path
            
            # Construire la route Starlette
            starlette_route = self._build_route(
                full_path,
                route_info.func,
                route_info.methods,
                all_tags
            )
            
            # Ajouter la route
            self.routes.append(starlette_route)
            self._routes_info.append(route_info)
        
        logger.info(f"Router inclus avec {len(router.get_routes())} routes")
    
    def get(self, path: str, **kwargs):
        """Décorateur pour route GET"""
        return self.route(path, methods=["GET"], **kwargs)
    
    def post(self, path: str, **kwargs):
        """Décorateur pour route POST"""
        return self.route(path, methods=["POST"], **kwargs)
    
    def put(self, path: str, **kwargs):
        """Décorateur pour route PUT"""
        return self.route(path, methods=["PUT"], **kwargs)
    
    def patch(self, path: str, **kwargs):
        """Décorateur pour route PATCH"""
        return self.route(path, methods=["PATCH"], **kwargs)
    
    def delete(self, path: str, **kwargs):
        """Décorateur pour route DELETE"""
        return self.route(path, methods=["DELETE"], **kwargs)
    
    def _build_route(
        self, 
        path: str, 
        func: Callable, 
        methods: List[str],
        tags: List[str] = []
    ) -> Route:
        """Construit une route Starlette"""
        route_info = RouteInfo(path, func, methods, tags)
        self._routes_info.append(route_info)
        
        async def endpoint(request: Request):
            try:
                # Validation des paramètres
                params = await RequestValidator.parse_request(request, func)
                
                # Résolution des dépendances
                deps = await self._dependency_manager.resolve(func)
                
                # Exécution de la fonction
                result = await self._call_endpoint(func, {**params, **deps})
                
                # Retour de la réponse
                if isinstance(result, (JSONResponse, HTMLResponse)):
                    return result
                
                return JSONResponse(result)
                
            except AppException as e:
                return JSONResponse(
                    {"error": e.message, "details": e.details},
                    status_code=e.status_code
                )
            except Exception as e:
                logger.error(f"Erreur dans {path}: {e}", exc_info=True)
                return JSONResponse(
                    {"error": "Internal server error"},
                    status_code=500
                )
        
        return Route(path, endpoint=endpoint, methods=methods)
    
    async def _call_endpoint(self, func: Callable, kwargs: Dict):
        """Appelle un endpoint (sync ou async)"""
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)
    
    # Gestion des exceptions
    async def _app_exception_handler(self, request: Request, exc: AppException):
        return JSONResponse(
            {"error": exc.message, "details": exc.details},
            status_code=exc.status_code
        )
    
    async def _validation_exception_handler(self, request: Request, exc: ValidationError):
        return JSONResponse(
            {"error": "Validation error", "details": exc.errors()},
            status_code=422
        )
    
    async def _generic_exception_handler(self, request: Request, exc: Exception):
        logger.error(f"Erreur non gérée: {exc}", exc_info=True)
        return JSONResponse(
            {"error": "Internal server error"},
            status_code=500
        )
    
    # Documentation OpenAPI
    def _register_docs(self):
        """Enregistre les routes de documentation"""
        async def openapi(request: Request):
            schema = self._generate_openapi()
            return JSONResponse(schema)
        
        async def docs(request: Request):
            html = self._swagger_ui_html()
            return HTMLResponse(html)
        
        async def redoc(request: Request):
            html = self._redoc_html()
            return HTMLResponse(html)
        
        self.routes.append(Route("/openapi.json", endpoint=openapi, methods=["GET"]))
        self.routes.append(Route("/docs", endpoint=docs, methods=["GET"]))
        self.routes.append(Route("/redoc", endpoint=redoc, methods=["GET"]))
    
    def _generate_openapi(self) -> Dict:
        """Génère le schéma OpenAPI"""
        paths = {}
        
        for info in self._routes_info:
            path_item = {}
            
            for method in info.methods:
                method_lower = method.lower()
                params, request_body = self._extract_schema(info.func)
                
                path_item[method_lower] = {
                    "summary": info.func.__name__,
                    "description": info.func.__doc__ or "",
                    "tags": info.tags,
                    "parameters": params,
                    "requestBody": request_body,
                    "responses": {
                        "200": {"description": "Successful Response"},
                        "422": {"description": "Validation Error"},
                        "500": {"description": "Internal Server Error"}
                    }
                }
            
            paths[info.path] = path_item
        
        return {
            "openapi": "3.0.2",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description
            },
            "paths": paths
        }
    
    def _extract_schema(self, func: Callable):
        """Extrait le schéma OpenAPI d'une fonction"""
        sig = inspect.signature(func)
        params = []
        request_body = None
        
        for param_name, param in sig.parameters.items():
            ann = param.annotation
            
            if RequestValidator._is_pydantic_model(ann):
                schema = ann.model_json_schema()
                request_body = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": schema
                        }
                    }
                }
            elif param_name not in ["request"] and param_name not in self._dependency_manager._dependencies:
                params.append({
                    "name": param_name,
                    "in": "query",
                    "required": param.default == inspect.Parameter.empty,
                    "schema": {"type": "string"}
                })
        
        return params, request_body
    
    def _swagger_ui_html(self) -> str:
        """Génère le HTML pour Swagger UI"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title} - Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui.min.css" />
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.min.js" crossorigin></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui-standalone-preset.min.js" crossorigin></script>
            <script>
                window.onload = function() {{
                    const ui = SwaggerUIBundle({{
                        url: '/openapi.json',
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        layout: "StandaloneLayout"
                    }});
                    window.ui = ui;
                }};
            </script>
        </body>
        </html>
        """
    
    def _redoc_html(self) -> str:
        """Génère le HTML pour ReDoc (alternative à Swagger)"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title} - ReDoc</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <redoc spec-url='/openapi.json'></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
        </body>
        </html>
        """