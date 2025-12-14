from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from authx.exceptions import CredentialsException

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allow_unsecure: list[str] = None):
        super().__init__(app)
        self.allow_unsecure = allow_unsecure or []

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in self.allow_unsecure:
            return await call_next(request)

        if "Authorization" not in request.headers:
            return JSONResponse(
                {"detail": "Missing Authorization header"}, status_code=401
            )
        
        # The actual token validation is done in the get_current_user dependency.
        # Here we just check for the presence of the header.
        
        response = await call_next(request)
        return response
