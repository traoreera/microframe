"""
HTTP request and exception handlers
"""
import inspect
import logging
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import ValidationError

from ..core.exceptions import MicroFrameException
from ..validation.parser import RequestParser

logger = logging.getLogger(__name__)


class ExceptionHandler:
    """Centralized exception handling"""
    
    async def handle_microframe_exception(
        self,
        request: Request,
        exc: MicroFrameException
    ) -> JSONResponse:
        """Handle framework exceptions"""
        return JSONResponse(
            exc.to_dict(),
            status_code=exc.status_code
        )
    
    async def handle_validation_error(
        self,
        request: Request,
        exc: ValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors"""
        return JSONResponse(
            {
                "message": "Validation error",
                "errors": exc.errors()
            },
            status_code=422
        )
    
    async def handle_generic_exception(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            {"message": "Internal server error"},
            status_code=500
        )


class RouteHandler:
    """Handler for route execution"""
    
    def __init__(self, route_info, dependency_manager):
        self.route_info = route_info
        self.dependency_manager = dependency_manager
        self.parser = RequestParser()
    
    async def handle(self, request: Request) -> JSONResponse:
        """Handle incoming request"""
        try:
            # Parse request parameters
            params = await self.parser.parse(request, self.route_info.func)
            
            # Resolve dependencies
            deps = await self.dependency_manager.resolve(
                self.route_info.func,
                request
            )
            
            # Merge parameters
            kwargs = {**params, **deps}
            
            # Execute endpoint
            result = await self._execute(kwargs)
            
            # Return response
            if isinstance(result, JSONResponse):
                return result
            
            return JSONResponse(
                result,
                status_code=self.route_info.status_code
            )
        
        except Exception:
            # Re-raise to be handled by exception handlers
            raise
    
    async def _execute(self, kwargs: Dict[str, Any]) -> Any:
        """Execute the endpoint function"""
        if inspect.iscoroutinefunction(self.route_info.func):
            return await self.route_info.func(**kwargs)
        return self.route_info.func(**kwargs)
