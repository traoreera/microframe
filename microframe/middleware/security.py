import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware de sécurité avec protection CSRF, XSS, et headers"""

    def __init__(self, app, config=None):
        super().__init__(app)
        self.config = config or {}
        self.rate_limiter = RateLimiter()

    async def dispatch(self, request, call_next):
        # Vérification de la méthode HTTP
        if request.method not in ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]:
            return JSONResponse({"error": "Method not allowed"}, status_code=405)

        # Rate limiting
        client_ip = request.client.host
        if not self.rate_limiter.check_rate_limit(client_ip):
            return JSONResponse({"error": "Too many requests"}, status_code=429)

        # Validation de la taille du contenu
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10_000_000:  # 10MB
            return JSONResponse({"error": "Payload too large"}, status_code=413)

        # Traitement de la requête
        response = await call_next(request)

        # Ajout des headers de sécurité
        response.headers.update(self._security_headers())

        return response

    def _security_headers(self):
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }


class RateLimiter:
    """Rate limiter simple basé sur la mémoire"""

    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def check_rate_limit(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Nettoyer les anciennes requêtes
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] if req_time > window_start
        ]

        # Vérifier la limite
        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True


class CORSMiddleware(BaseHTTPMiddleware):
    """Middleware CORS configurable"""

    def __init__(self, app, allow_origins=None, allow_methods=None, allow_headers=None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]

    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS":
            return self._preflight_response()

        response = await call_next(request)
        response.headers.update(self._cors_headers(request))
        return response

    def _cors_headers(self, request):
        origin = request.headers.get("origin", "*")
        if self.allow_origins != ["*"] and origin not in self.allow_origins:
            origin = self.allow_origins[0]

        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
            "Access-Control-Allow-Headers": ", ".join(self.allow_headers),
            "Access-Control-Max-Age": "3600",
        }

    def _preflight_response(self):
        return JSONResponse({}, headers=self._cors_headers(None))
