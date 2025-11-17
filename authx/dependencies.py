"""_summary_

    Raises:
        CredentialsException: this exception is raised when the token is invalid or missing
        UserNotFoundException: this exception is raised when the user is not found

    Returns:
        _type_: _description_
"""

from inspect import signature
from typing import Annotated, Callable, TypeVar

from annotated_doc import Doc
from starlette.requests import Request

from authx.config import AuthConfig
from authx.exceptions import CredentialsException, UserNotFoundException
from authx.jwt import decode_token
from authx.manager import AuthManager
from authx.models import UserResponse

T = TypeVar("T")


# TODO:you can use it like this or other Depends injection
class Depends:
    """Classe pour gérer les dépendances d'injection"""

    def __init__(self, dependency: Annotated[Callable, Doc("Dependancy for injection")]):
        self.dependency = dependency


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
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return CredentialsException("Token manquant ou invalide").__dict__

    token = auth_header.replace("Bearer ", "")

    config: AuthConfig = request.app.state.auth_config
    manager: AuthManager = request.app.state.auth_manager

    payload = decode_token(token, config, "access")
    user_id = payload.get("sub")

    if not user_id:
        return CredentialsException("Token invalide").__dict__

    user = await manager.get_user_by_id(user_id)
    if not user:
        return UserNotFoundException().__dict__

    return user


async def resolve_dependencies(request: Request, handler: Callable) -> dict:
    """
    Résout les dépendances d'une fonction handler

    Args:
        request: Requête Starlette
        handler: Fonction handler avec potentiellement des Depends()

    Returns:
        Dictionnaire des arguments résolus
    """
    sig = signature(handler)
    kwargs = {}

    for param_name, param in sig.parameters.items():
        if param_name == "request":
            kwargs[param_name] = request
        elif isinstance(param.default, Depends):
            dependency_func = param.default.dependency
            # Résoudre récursivement les dépendances
            if signature(dependency_func).parameters.get("request"):
                kwargs[param_name] = await dependency_func(request)
            else:
                kwargs[param_name] = await dependency_func()

    return kwargs
