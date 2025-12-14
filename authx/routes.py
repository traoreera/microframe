from typing import TYPE_CHECKING

from starlette.requests import Request
from starlette.responses import JSONResponse

from authx.config import AuthConfig
from authx.dependencies import get_current_user
from authx.exceptions import CredentialsException
from authx.jwt import create_access_token, create_refresh_token, decode_token
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse

if TYPE_CHECKING:
    from microframe import Router

# Router will be lazily created to avoid circular imports
auth_router = None


def create_auth_router():
    """Factory function to create auth router, avoiding circular imports."""
    from microframe import Router
    
    router = Router(prefix="/auth", tags=["Authentication"])
    
    @router.post("/login", response_model=TokenResponse)
    async def login(request: Request, user: LoginRequest):
        return await _login(request, user)
    
    @router.get("/me", response_model=UserResponse)
    async def get_me(request: Request):
        current_user = await get_current_user(request)
        return current_user
    
    @router.post("/refresh", response_model=TokenResponse)
    async def refresh_token(request: Request):
        return await _refresh(request)
    
    @router.post("/logout")
    async def logout_user(request: Request):
        return await _logout(request)
    
    return router


async def _login(request: Request, user: LoginRequest):
    """
    User login handler.
    """
    manager: AuthManager = request.app.state.auth_manager
    auth_config: AuthConfig = request.app.state.auth_config
    
    if user_data := await manager.authenticate(user.email, user.password):
        refresh_token = create_refresh_token(user_data.get("id"), auth_config)
        access_token = create_access_token(user_data.get("id"), auth_config)
        
        token_response = TokenResponse(access_token=access_token, refresh_token=refresh_token)
        
        response = JSONResponse(token_response.dict())
        response.set_cookie(
            key=auth_config.cookie_name,
            value=refresh_token,
            httponly=auth_config.cookie_httponly,
            secure=auth_config.cookie_secure,
            samesite=auth_config.cookie_samesite,
        )
        return response
    else:
        raise CredentialsException("Invalid credentials")


async def _refresh(request: Request):
    """
    Refresh access token handler.
    """
    auth_config: AuthConfig = request.app.state.auth_config
    refresh_token = request.cookies.get(auth_config.cookie_name)

    if not refresh_token:
        raise CredentialsException("Missing refresh token.")

    payload = decode_token(refresh_token, auth_config, "refresh")
    user_id = payload.get("sub")

    if not user_id:
        raise CredentialsException("Invalid refresh token.")

    access_token = create_access_token(user_id, auth_config)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


async def _logout(request: Request):
    """
    Logout handler.
    """
    auth_config: AuthConfig = request.app.state.auth_config
    response = JSONResponse({"message": "Successfully logged out"})
    response.delete_cookie(auth_config.cookie_name)
    return response

