"""
CORS middleware
"""
from typing import List

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response
from starlette.requests import Request


class CORSMiddleware(BaseHTTPMiddleware):
    """
    CORS (Cross-Origin Resource Sharing) middleware
    
    Example:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["GET", "POST"],
            allow_headers=["*"]
        )
    """
    
    def __init__(
        self,
        app,
        allow_origins: List[str] = None,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None,
        allow_credentials: bool = False,
        max_age: int = 3600
    ):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_credentials = allow_credentials
        self.max_age = max_age
    
    async def dispatch(self, request: Request, call_next):
        """Handle CORS headers"""
        # Handle preflight requests
        if request.method == "OPTIONS":
            return self._preflight_response(request)
        
        # Process request
        response = await call_next(request)
        
        # Add CORS headers
        self._add_cors_headers(request, response)
        
        return response
    
    def _add_cors_headers(self, request: Request, response: Response):
        """Add CORS headers to response"""
        origin = request.headers.get("origin", "*")
        
        # Check if origin is allowed
        if self.allow_origins != ["*"] and origin not in self.allow_origins:
            origin = self.allow_origins[0] if self.allow_origins else "*"
        
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        response.headers["Access-Control-Max-Age"] = str(self.max_age)
        
        if self.allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"
    
    def _preflight_response(self, request: Request) -> Response:
        """Handle preflight OPTIONS request"""
        headers = {}
        origin = request.headers.get("origin", "*")
        
        if self.allow_origins != ["*"] and origin not in self.allow_origins:
            origin = self.allow_origins[0] if self.allow_origins else "*"
        
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        headers["Access-Control-Max-Age"] = str(self.max_age)
        
        if self.allow_credentials:
            headers["Access-Control-Allow-Credentials"] = "true"
        
        return JSONResponse({}, headers=headers)
