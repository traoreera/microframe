from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from ws import BaseWebSocket

from authx.config import AuthConfig
from authx.dependencies import get_current_user
from authx.jwt import create_access_token, create_refresh_token
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse
from authx.security import hash_password, verify_password
from microframe import Router

# ---------------------------
# Mock database / AuthManager
# ---------------------------


class MockAuthManager(AuthManager):
    def __init__(self):
        # Dummy user
        self.users = {
            "user@example.com": {
                "id": "42",
                "email": "user@example.com",
                "password_hash": hash_password("password123"),
            }
        }

    async def get_user_by_email(self, email: str):
        user = self.users.get(email)
        if user:
            return UserResponse(id=user["id"], email=user["email"])
        return None

    async def get_user_by_id(self, user_id: str):
        for user in self.users.values():
            if user["id"] == user_id:
                return UserResponse(id=user["id"], email=user["email"])
        return None

    async def verify_password(self, email: str, password: str):
        user = self.users.get(email)
        if not user:
            return False
        return verify_password(password, user["password_hash"])


# ---------------------------
# AuthX configuration
# ---------------------------
auth_config = AuthConfig(secret_key="supersecretjwtkey")
auth_manager = MockAuthManager()


# ---------------------------
# API Routes
# ---------------------------

router = Router(prefix="/api", tags=["API"])


@router.post("/login")
async def login(request: Request, user: LoginRequest):

    user = await auth_manager.authenticate(user.email, user.password)
    if not user:
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    access_token = create_access_token(user.id, auth_config)
    refresh_token = create_refresh_token(user.id, auth_config)
    response = TokenResponse(access_token=access_token, refresh_token=refresh_token)
    return JSONResponse(response.response_model)


@router.get("/protected")
async def protected(request: Request):
    # Dependency injection example
    user: UserResponse = await get_current_user(request)
    if isinstance(user, dict):
        return user
    return JSONResponse({"message": f"Hello {user.email}!"})


# ---------------------------
# WebSocket Example
# ---------------------------
class ChatWebSocket(BaseWebSocket):
    async def on_message(self, websocket, user_id, message):
        # Echo back to the user
        await websocket.send_json({"user": user_id, "message": message})

    async def on_connect(self, websocket, user_id):
        print(f"{user_id} connected to WebSocket")

    async def on_disconnect(self, websocket, user_id):
        print(f"{user_id} disconnected from WebSocket")

    async def on_receive(self, websocket: WebSocket):
        return await websocket.receive_json()


# Configure WebSocket with AuthX
ChatWebSocket.configure(auth_config=auth_config, auth_manager=auth_manager)
