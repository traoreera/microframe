from typing import Optional

from pydantic import BaseModel, Field

from authx.config import AuthConfig
from authx.dependencies import Depends, get_current_user
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse
from microframe import Request, Router, status
from authx.routes import login_servise, me_service
router = Router(prefix="/auth", tags=["Auth"], dependencies=[Request])


class MyDb(AuthManager):

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        return UserResponse(id="1", email=email)

    async def verify_password(self, email: str, password: str) -> bool:
        return True

    async def authenticate(self, email: str, password: str) -> Optional[UserResponse]:
        return UserResponse(id="1", email=email)

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        return UserResponse(id="1", email="user@example.com")


@router.post("/login", response_model=UserResponse)
async def login(request: Request, user: LoginRequest):

    return await login_servise(request, user)

@router.get("/me", response_model=UserResponse)
async def me(request):
    
    return await me_service(request=request, current_user=get_current_user)