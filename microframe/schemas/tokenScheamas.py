from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Token d'accès"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données contenues dans le token"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    roles: list[str] = []
