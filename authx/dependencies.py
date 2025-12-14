from starlette.requests import Request
from authx.config import AuthConfig
from authx.exceptions import CredentialsException, UserNotFoundException
from authx.jwt import decode_token
from authx.models import UserResponse
from authx.manager import AuthManager


async def get_current_user(request: Request) -> UserResponse:
    """
    Retrieves the current user from the access token.

    Args:
        request: The Starlette request.

    Returns:
        The authenticated user as a UserResponse object.

    Raises:
        CredentialsException: If the token is invalid or missing.
        UserNotFoundException: If the user does not exist.
    """
    auth_config: AuthConfig = request.app.state.auth_config
    auth_manager: AuthManager = request.app.state.auth_manager

    token = None
    if auth_header := request.headers.get("Authorization"):
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise CredentialsException("Missing authentication token.")

    payload = decode_token(token, auth_config, "access")
    user_id = payload.get("sub")

    if not user_id:
        raise CredentialsException("Invalid token payload.")

    user = await auth_manager.get_user_by_id(user_id)
    if not user:
        raise UserNotFoundException(f"User with id {user_id} not found.")

    return UserResponse(**user)
