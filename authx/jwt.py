"""
    Decodes a JWT token and returns the payload.

    Raises:
        InvalidTokenException: If the token is invalid or malformed.
        TokenExpiredException: If the token has expired.

    Returns:
        dict: The decoded payload.
"""

from jose import JWTError, jwt
from authx.config import AuthConfig
from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Optional
from authx.exceptions import InvalidTokenException, TokenExpiredException


def create_token(
    data: Dict[str, Any],
    config: AuthConfig,
    token_type: Literal["access", "refresh"],
    expires_delta: timedelta,
) -> str:
    """
        Crée un JWT token
        # Arguments
            `data`: Les données du token
            `config`: La configuration d'authentification
            `token_type`: Le type de token ("access" ou "refresh")
            `expires_delta`: La durée de validité du token
    """
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode |= {"exp": expire, "iat": datetime.now(), "type": token_type}


    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)


def create_access_token(data: Optional[str | Dict], config: AuthConfig) -> str:
    """
        Crée un access token
        # Arguments
            `data`: L'identifiant de l'utilisateur
            `config`: La configuration d'authentification
    """
    return create_token(
        {"sub": data},
        config,
        "access",
        config.access_token_expire,
    )


def create_refresh_token(data: str, config: AuthConfig) -> str:
    """
        Crée un refresh token
        # Arguments
            `data`: L'identifiant de l'utilisateur
            `config`: La configuration d'authentification
    """
    return create_token(
        {"sub": data},
        config,
        "refresh",
        config.refresh_token_expire,
    )


def decode_token(
    token: str, config: AuthConfig, expected_type: Literal["access", "refresh"]
) -> Dict[str, Any]:
    """
        Décode et valide un JWT token
        # Arguments
            `token`: Le token JWT
            `config`: La configuration d'authentification
            `expected_type`: Le type de token attendu
    """
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])

        if payload.get("type") != expected_type:
            raise InvalidTokenException("Type de token invalide")

        return payload
    except JWTError as e:
        raise TokenExpiredException("Token expiré") from e
