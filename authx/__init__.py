"""
Starlette AuthX - Module d'authentification JWT pour Starlette
"""

__version__ = "0.1.0"

from authx.config import AuthConfig
from authx.dependencies import Depends, get_current_user
from authx.exceptions import (
    AuthException,
    CredentialsException,
    InvalidTokenException,
    TokenExpiredException,
)
from authx.manager import AuthManager
from authx.models import TokenResponse, UserResponse
from authx.security import hash_password, verify_password

__all__ = [
    "AuthConfig",
    "AuthManager",
    "Depends",
    "get_current_user",
    "TokenResponse",
    "UserResponse",
    "AuthException",
    "CredentialsException",
    "InvalidTokenException",
    "TokenExpiredException",
    "verify_password",
    "hash_password",
]
