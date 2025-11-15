from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from authx.config import AuthConfig
from authx.dependencies import Depends, get_current_user, resolve_dependencies
from authx.exceptions import CredentialsException, InvalidTokenException
from authx.jwt import create_access_token, create_refresh_token, decode_token
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse


async def login_servise(request: Request, user: LoginRequest) -> JSONResponse:
    """Endpoint de connexion"""

    config: AuthConfig = request.app.state.auth_config
    manager: AuthManager = request.app.state.auth_manager

    data = await manager.authenticate(user.email, user.password)
    if not data:
        raise CredentialsException()

    access_token = create_access_token(data.id, config)
    refresh_token = create_refresh_token(data.id, config)



    response = JSONResponse(
        TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        ).model_dump()
    )

    # Stocker le refresh token dans un cookie HttpOnly
    response.set_cookie(
        key=config.cookie_name,
        value=refresh_token,
        httponly=config.cookie_httponly,
        secure=config.cookie_secure,
        samesite=config.cookie_samesite,
        max_age=int(config.refresh_token_expire.total_seconds()),
    )

    return response


async def refresh_service(request: Request) -> JSONResponse:
    """Endpoint de rafraîchissement du token"""
    config: AuthConfig = request.app.state.auth_config
    manager: AuthManager = request.app.state.auth_manager

    refresh_token = request.cookies.get(config.cookie_name)
    if not refresh_token:
        raise InvalidTokenException("Refresh token manquant")

    payload = decode_token(refresh_token, config, "refresh")
    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenException()

    user = await manager.get_user_by_id(user_id)
    if not user:
        raise CredentialsException()

    access_token = create_access_token(user.id, config)

    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


async def me_service(
    request: Request, current_user: UserResponse = Depends(get_current_user)
) -> JSONResponse:
    """Endpoint pour récupérer les informations de l'utilisateur connecté"""
    kwargs = await resolve_dependencies(request, me_service)
    current_user = kwargs.get("current_user")

    return JSONResponse(current_user.model_dump())
