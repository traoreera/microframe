from datetime import datetime, timedelta
from typing import Any, Dict

from jose import JWTError, jwt

from authx.config import AuthConfig
from authx.exceptions import InvalidTokenException, TokenExpiredException


def create_token(
    data: Dict[str, Any], config: AuthConfig, token_type: str, expires_delta: timedelta
) -> str:
    """Crée un JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": token_type})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt


def create_access_token(user_id: str, config: AuthConfig) -> str:
    """Crée un access token"""
    return create_token(
        {"sub": user_id},
        config,
        "access",
        config.access_token_expire,
    )


def create_refresh_token(user_id: str, config: AuthConfig) -> str:
    """Crée un refresh token"""
    return create_token(
        {"sub": user_id},
        config,
        "refresh",
        config.refresh_token_expire,
    )


def decode_token(token: str, config: AuthConfig, expected_type: str) -> Dict[str, Any]:
    """Décode et valide un JWT token"""
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])

        if payload.get("type") != expected_type:
            raise InvalidTokenException("Type de token invalide")

        return payload
    except JWTError:
        raise TokenExpiredException()
    except JWTError:
        raise InvalidTokenException()
