import asyncio
import time
from collections import defaultdict
from typing import Dict, List, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = asyncio.Lock()

    async def check(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window

        async with self.lock:
            self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
            if len(self.requests[client_id]) >= self.max_requests:
                return False
            self.requests[client_id].append(now)
            return True


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        rate_limit_requests: int = 100,
        rate_limit_window: int = 60,
        max_content_length: int = 10_000_000,
        allowed_methods: Optional[List[str]] = None,
    ):
        super().__init__(app)
        self.rate_limiter = RateLimiter(rate_limit_requests, rate_limit_window)
        self.max_content_length = max_content_length
        self.allowed_methods = allowed_methods or [
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ]

    async def dispatch(self, request: Request, call_next):
        client_ip = (
            request.headers.get("x-forwarded-for", request.client.host).split(",")[0].strip()
        )

        if request.method not in self.allowed_methods:
            return JSONResponse({"detail": "Method not allowed"}, status_code=405)

        if not await self.rate_limiter.check(client_ip):
            return JSONResponse({"detail": "Too many requests"}, status_code=429)

        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_content_length:
            return JSONResponse({"detail": "Payload too large"}, status_code=413)

        response = await call_next(request)

        for k, v in SECURITY_HEADERS.items():
            response.headers[k] = v

        return response
