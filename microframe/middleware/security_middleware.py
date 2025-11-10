"""
Security middleware with rate limiting
"""
import time
from collections import defaultdict
from typing import Dict, List

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware with rate limiting and security headers
    
    Example:
        app.add_middleware(
            SecurityMiddleware,
            rate_limit_requests=100,
            rate_limit_window=60,
            max_content_length=10_000_000
        )
    """
    
    def __init__(
        self,
        app,
        rate_limit_requests: int = 100,
        rate_limit_window: int = 60,
        max_content_length: int = 10_000_000,
        allowed_methods: List[str] = None
    ):
        super().__init__(app)
        self.rate_limiter = RateLimiter(rate_limit_requests, rate_limit_window)
        self.max_content_length = max_content_length
        self.allowed_methods = allowed_methods or ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    
    async def dispatch(self, request: Request, call_next):
        """Apply security checks"""
        # Check HTTP method
        if request.method not in self.allowed_methods:
            return JSONResponse(
                {"error": "Method not allowed"},
                status_code=405
            )
        
        # Rate limiting
        client_ip = request.client.host if request.client else "unknown"
        if not self.rate_limiter.check(client_ip):
            return JSONResponse(
                {"error": "Too many requests"},
                status_code=429
            )
        
        # Content length check
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_content_length:
            return JSONResponse(
                {"error": "Payload too large"},
                status_code=413
            )
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        self._add_security_headers(response)
        
        return response
    
    def _add_security_headers(self, response):
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def check(self, client_id: str) -> bool:
        """Check if request is within rate limit"""
        now = time.time()
        window_start = now - self.window
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Record request
        self.requests[client_id].append(now)
        return True
    
    def reset(self, client_id: str):
        """Reset rate limit for client"""
        if client_id in self.requests:
            del self.requests[client_id]
