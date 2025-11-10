"""
Core application class
"""
import logging
from typing import Any, Callable, Dict, List, Optional

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from pydantic import ValidationError

from .config import AppConfig
from .exceptions import MicroFrameException, ValidationException
from ..routing.router import Router
from ..routing.registry import RouteRegistry
from ..dependencies.manager import DependencyManager
from ..docs.openapi import OpenAPIGenerator
from ..http.handlers import ExceptionHandler

logger = logging.getLogger(__name__)


class Application(Starlette):
    """
    Main application class
    
    Example:
        app = Application(
            title="My API",
            version="1.0.0",
            description="A simple API"
        )
        
        @app.get("/")
        async def index():
            return {"message": "Hello World"}
    """
    
    def __init__(
        self,
        title: str = "MicroFramework",
        version: str = "1.0.0",
        description: str = "",
        debug: bool = False,
        config: Optional[AppConfig] = None,
        middleware: Optional[List[Middleware]] = None
    ):
        # Initialize configuration
        self.config = config or AppConfig(
            title=title,
            version=version,
            description=description,
            debug=debug
        )
        
        # Initialize core components
        self.dependency_manager = DependencyManager()
        self.route_registry = RouteRegistry()
        self.exception_handler = ExceptionHandler()
        self.openapi_generator = OpenAPIGenerator(self.config)
        
        # Initialize Starlette
        super().__init__(
            debug=self.config.debug,
            routes=[],
            middleware=middleware or [],
            exception_handlers=self._build_exception_handlers()
        )
        
        # Register documentation routes
        self._register_docs()
        
        logger.info(f"Application '{self.config.title}' initialized")
    
    def _build_exception_handlers(self) -> Dict:
        """Build exception handlers dictionary"""
        return {
            MicroFrameException: self.exception_handler.handle_microframe_exception,
            ValidationError: self.exception_handler.handle_validation_error,
            Exception: self.exception_handler.handle_generic_exception
        }
    
    def include_router(
        self,
        router: Router,
        prefix: str = "",
        tags: Optional[List[str]] = None
    ):
        """
        Include a router in the application
        
        Args:
            router: Router instance to include
            prefix: URL prefix for all routes
            tags: Additional tags for all routes
        """
        routes = router.get_routes(prefix=prefix, tags=tags)
        
        for route_info in routes:
            # Build Starlette route
            starlette_route = self._build_route(route_info)
            self.routes.append(starlette_route)
            
            # Register in registry
            self.route_registry.register(route_info)
        
        logger.info(f"Router included with {len(routes)} routes")
    
    def _build_route(self, route_info) -> Route:
        """Build a Starlette route from RouteInfo"""
        from ..http.handlers import RouteHandler
        
        handler = RouteHandler(
            route_info=route_info,
            dependency_manager=self.dependency_manager
        )
        
        return Route(
            route_info.path,
            endpoint=handler.handle,
            methods=route_info.methods
        )
    
    def route(
        self,
        path: str,
        methods: Optional[List[str]] = None,
        **kwargs
    ) -> Callable:
        """Decorator to register a route"""
        from ..routing.decorators import route_decorator
        
        def decorator(func: Callable) -> Callable:
            route_info = route_decorator(
                path=path,
                func=func,
                methods=methods or ["GET"],
                **kwargs
            )
            
            # Build and add route
            starlette_route = self._build_route(route_info)
            self.routes.append(starlette_route)
            self.route_registry.register(route_info)
            
            logger.info(f"Route registered: {methods or ['GET']} {path}")
            return func
        
        return decorator
    
    def get(self, path: str, **kwargs) -> Callable:
        """GET route decorator"""
        return self.route(path, methods=["GET"], **kwargs)
    
    def post(self, path: str, **kwargs) -> Callable:
        """POST route decorator"""
        return self.route(path, methods=["POST"], **kwargs)
    
    def put(self, path: str, **kwargs) -> Callable:
        """PUT route decorator"""
        return self.route(path, methods=["PUT"], **kwargs)
    
    def patch(self, path: str, **kwargs) -> Callable:
        """PATCH route decorator"""
        return self.route(path, methods=["PATCH"], **kwargs)
    
    def delete(self, path: str, **kwargs) -> Callable:
        """DELETE route decorator"""
        return self.route(path, methods=["DELETE"], **kwargs)
    
    def dependency(self, name: Optional[str] = None, cache: bool = False) -> Callable:
        """Decorator to register a dependency"""
        def decorator(func: Callable) -> Callable:
            dep_name = name or func.__name__
            self.dependency_manager.register(dep_name, func, cache=cache)
            return func
        return decorator
    
    def _register_docs(self):
        """Register documentation routes"""
        if self.config.openapi_url:
            async def openapi(request: Request):
                schema = self.openapi_generator.generate(
                    self.route_registry.get_all()
                )
                return JSONResponse(schema)
            
            self.routes.append(
                Route(self.config.openapi_url, endpoint=openapi, methods=["GET"])
            )
        
        if self.config.docs_url:
            from ..docs.ui import SwaggerUI
            swagger_ui = SwaggerUI(self.config)
            
            async def docs(request: Request):
                return swagger_ui.render()
            
            self.routes.append(
                Route(self.config.docs_url, endpoint=docs, methods=["GET"])
            )
        
        if self.config.redoc_url:
            from ..docs.ui import ReDocUI
            redoc_ui = ReDocUI(self.config)
            
            async def redoc(request: Request):
                return redoc_ui.render()
            
            self.routes.append(
                Route(self.config.redoc_url, endpoint=redoc, methods=["GET"])
            )
