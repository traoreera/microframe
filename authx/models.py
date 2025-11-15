from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Modèle de requête pour la connexion"""

    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Modèle de réponse pour les tokens"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Modèle de réponse pour les informations utilisateur"""

    id: str
    email: str
    data: Optional[Dict[str, Any]] = None


class TokenPayload(BaseModel):
    """Modèle pour le payload du JWT"""

    sub: str  # user_id
    type: str  # "access" ou "refresh"
    exp: int
    iat: int
