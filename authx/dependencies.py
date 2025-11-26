"""_summary_

    Raises:
        CredentialsException: this exception is raised when the token is invalid or missing
        UserNotFoundException: this exception is raised when the user is not found

    Returns:
        _type_: _description_
"""

from typing import TypeVar

from annotated_doc import Doc
from starlette.requests import Request

from authx.config import AuthConfig
from authx.exceptions import CredentialsException, UserNotFoundException
from authx.jwt import decode_token
from authx.manager import AuthManager
from authx.models import UserResponse

T = TypeVar("T")


# TODO: if you wanted to use that you need to await the function before using it
async def get_current_user(request: Request) -> UserResponse | dict:
    """
    Récupère l'utilisateur courant depuis le token d'accès

    Args:
        request: Requête Starlette

    Returns:
        UserResponse de l'utilisateur authentifié

    Raises:
        CredentialsException: Si le token est invalide ou manquant
        UserNotFoundException: Si l'utilisateur n'existe pas
    """

    auth: AuthConfig = request.app.state.auth_configure

    if auth_header := request.headers.get("Authorization"):
        auth_header.removeprefix("Bearer ")
        token = decode_token(auth_header, auth, "access")

        return user

    if token := request.session["user"]["access_token"]:
        user = decode_token(token, auth, "access")
        return user

    raise CredentialsException


async def get_current_reloaded_user(request: Request) -> UserResponse | dict:
    """
    Récupère l'utilisateur courant depuis le token d'accès

    Args:
        request: Requête Starlette

    Returns:
        UserResponse de l'utilisateur authentифiado
    """
    auth: AuthConfig = request.app.state.auth_configure

    if auth_header := request.headers.get("Authorization"):
        auth_header.removeprefix("Bearer ")
        token = decode_token(auth_header, auth, "access")

        return user

    if token := request.session["user"]["access_token"]:
        user = decode_token(token, auth, "refresh")
        return user

    raise CredentialsException
