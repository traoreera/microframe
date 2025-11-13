from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Token d'accès"""

    access_token: str = Field(..., alias="accessToken", title="Token d'accès")
    refresh_token: str = Field(..., alias="refreshToken", title="Token de rafraîchissement")
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données contenues dans le token"""

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []
