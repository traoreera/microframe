from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Modèle de requête pour la connexion"""

    email: EmailStr = Field(
        ..., min_length=8, max_length=50, description="user email", title="Email"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="user password",
        title="Password",
    )

    @property
    def response_model(self) -> Dict[str, Any]:
        """Response Model for LoginRequest"""
        return {
            "email": self.email,
            "password": self.password,
        }


class TokenResponse(BaseModel):
    """Modèle de réponse pour les tokens"""

    access_token: str = Field(..., title="Access token", min_length=20, max_length=200)
    refresh_token: str = Field(..., title="refresh token")
    token_type: str = "bearer"  # Field(..., title="Type de token")

    @property
    def response_model(self) -> Dict[str, Any]:
        """Response Model for TokenResponse"""
        return {
            "accessToken": self.access_token,
            "refreshToken": self.refresh_token,
            "tokenType": self.token_type,
        }


class UserResponse(BaseModel):
    """Modèle de réponse pour les informations utilisateur"""

    id: str = Field(..., min_length=1, max_length=30)
    email: str = Field(..., min_length=8, max_length=50)
    data: Optional[Dict[str, Any]] = None

    @property
    def response_model(self) -> Dict[str, Any]:
        """Response Model for UserResponse"""
        return {
            "id": self.id,
            "email": self.email,
            "data": self.data,
        }


class TokenPayload(BaseModel):
    """Modèle pour le payload du JWT"""

    sub: str = Field(
        ..., description="user id in the database", title="User id", min_length=1, max_length=30
    )
    type: str = Field(
        ..., description="Tooken types", title="Token type", min_length=1, max_length=30
    )
    exp: int = Field(..., description="Expiration time")
    iat: int = Field(..., description="Issued at")

    @property
    def response_model(self) -> Dict[str, Any]:
        """Response Model for TokenPayload"""
        return {
            "sub": self.sub,
            "type": self.type,
            "exp": self.exp,
            "iat": self.iat,
        }

    def __repr__(self) -> str:
        return f"TokenPayload(sub={self.sub}, type={self.type}, exp={self.exp}, iat={self.iat})"
