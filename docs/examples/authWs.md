# AuthX — Starlette JWT Authentication Module

**AuthX** is a lightweight, secure, and highly extensible JWT-based authentication module for Starlette and other ASGI frameworks.
It provides authentication services, dependency injection, WebSocket support, and secure password handling.

---

## 🌟 Features

* JWT authentication (access + refresh tokens)
* Password hashing & verification with bcrypt
* Abstract `AuthManager` interface for custom backends
* Request/response models with Pydantic
* Dependency injection for handlers
* WebSocket manager with JWT authentication & room support
* Exception handling for common auth errors
* Fully async, secure, and extensible

---

## ⚙️ Installation

```bash
pip install authx bcrypt python-jose pydantic starlette
```

---

## 📝 Configuration

Use the `AuthConfig` class to configure authentication parameters:

```python
from authx.config import AuthConfig

auth_config = AuthConfig(
    secret_key="super-secret-key-that-is-long",
    algorithm="HS256",
    access_token_expire_minutes=15,
    refresh_token_expire_days=7,
    cookie_name="refresh_token",
)
```

Key options:

| Parameter                     | Type | Default         | Description                    |
| ----------------------------- | ---- | --------------- | ------------------------------ |
| `secret_key`                  | str  | —               | Secret for signing tokens      |
| `algorithm`                   | str  | "HS256"         | JWT signing algorithm          |
| `access_token_expire_minutes` | int  | 15              | Lifetime of access tokens      |
| `refresh_token_expire_days`   | int  | 7               | Lifetime of refresh tokens     |
| `cookie_name`                 | str  | "refresh_token" | Cookie name for refresh tokens |
| `cookie_secure`               | bool | True            | Use secure cookies             |
| `cookie_httponly`             | bool | True            | Restrict JS access             |
| `cookie_samesite`             | str  | "strict"        | SameSite policy                |

---

## 🚨 Exceptions

AuthX provides dedicated exceptions for authentication flows:

| Exception               | Description         | HTTP Status |
| ----------------------- | ------------------- | ----------- |
| `AuthException`         | Base auth error     | 401         |
| `CredentialsException`  | Invalid credentials | 401         |
| `InvalidTokenException` | Token invalid       | 401         |
| `TokenExpiredException` | Token expired       | 401         |
| `UserNotFoundException` | User not found      | 404         |

---

## 🧠 AuthManager Interface

Abstract class for user management. Implement it to integrate with your DB:

```python
class AuthManager(ABC):
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]: ...
    async def get_user_by_id(self, user_id: Any) -> Optional[UserResponse]: ...
    async def verify_password(self, email: str, password: str) -> bool: ...
    async def authenticate(self, email: str, password: str) -> Optional[UserResponse]: ...
```

Example:

```python
from passlib.context import CryptContext

class SQLiteAuthManager(AuthManager):
    def __init__(self, db):
        self.db = db
        self.password_context = CryptContext(schemes=["bcrypt"])

    async def get_user_by_email(self, email: str):
        return await self.db.fetch_user(email=email)

    async def get_user_by_id(self, user_id: str):
        return await self.db.fetch_user(id=user_id)

    async def verify_password(self, email: str, password: str) -> bool:
        user = await self.get_user_by_email(email)
        return user and self.password_context.verify(password, user.password_hash)
```

---

## 🔑 JWT Utilities

Create and validate tokens:

```python
from authx.jwt import create_access_token, create_refresh_token, decode_token

access_token = create_access_token(user_id="42", config=auth_config)
refresh_token = create_refresh_token(user_id="42", config=auth_config)

payload = decode_token(access_token, config=auth_config, expected_type="access")
```

---

## 🔐 Password Utilities

Secure password handling with bcrypt:

```python
from authx.security import hash_password, verify_password

hashed = hash_password("mysecretpassword")
valid = verify_password("mysecretpassword", hashed)
```

---

## 📦 Pydantic Models

Models for requests, responses, and JWT payloads.

* `LoginRequest`: Email & password input
* `TokenResponse`: `access_token`, `refresh_token`, `token_type`
* `UserResponse`: `id`, `email`, optional `data`
* `TokenPayload`: JWT payload claims (`sub`, `type`, `exp`, `iat`)

Example:

```json
{
  "accessToken": "...",
  "refreshToken": "...",
  "tokenType": "bearer"
}
```

---

## 🌐 WebSocket Manager

`BaseWebSocket` provides JWT-authenticated WebSocket support with room/group management.

Key features:

* Auth via query params, cookie, or header
* `on_connect`, `on_message`, `on_disconnect` hooks
* Connection & room management
* Broadcast & targeted messaging

Usage:

```python
from starlette.routing import WebSocketRoute

class MyWebSocket(BaseWebSocket):
    async def on_message(self, websocket, user_id, message):
        await websocket.send_json({"echo": message})

routes = [WebSocketRoute("/ws", MyWebSocket())]
```

---

## 🧩 Dependency Injection

Use `Depends` to inject dependencies into handlers:

```python
from authx.dependencies import Depends

async def handler(request, current_user=Depends(get_current_user)):
    return {"user": current_user.email}
```

`get_current_user` extracts the user from the JWT token:

```python
from authx.dependencies import get_current_user
```

---

## 💡 Example Flow

1. User logs in via `/login` → `LoginRequest`
2. `AuthManager` verifies credentials
3. `create_access_token` + `create_refresh_token` issued
4. Client uses `access_token` in requests or WebSocket connection
5. AuthX validates tokens and provides `UserResponse`

---

## 🔮 Extensibility

* Custom AuthManager backends (SQL, NoSQL, SSO)
* Custom WebSocket hooks (`on_message`, `on_connect`, `on_disconnect`)
* Role & permission models
* Integrate with automatic OpenAPI generation

---

## ⚡ Notes

* Fully **async-ready** for Starlette/ASGI
* High performance, secure, and modular
* Tokens can be rotated, revoked, and extended

---

This README now serves as a **single source of truth** for AuthX’s usage, configuration, and integration.

## 📌 Example: AuthX + WebSocket

```python 
# main.py
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route, WebSocketRoute
from starlette.middleware.cors import CORSMiddleware

from authx.config import AuthConfig
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse
from authx.jwt import create_access_token, create_refresh_token
from authx.dependencies import get_current_user
from ws import BaseWebSocket
from authx.security import verify_password, hash_password

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
async def login(request: Request):
    body = await request.json()
    login_data = LoginRequest(**body)
    user = await auth_manager.authenticate(login_data.email, login_data.password)
    if not user:
        return JSONResponse({"error": "Invalid credentials"}, status_code=401)

    access_token = create_access_token(user.id, auth_config)
    refresh_token = create_refresh_token(user.id, auth_config)
    response = TokenResponse(access_token=access_token, refresh_token=refresh_token)
    return JSONResponse(response.response_model)


async def protected(request: Request):
    # Dependency injection example
    user: UserResponse = await get_current_user(request)
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


# Configure WebSocket with AuthX
ChatWebSocket.configure(auth_config=auth_config, auth_manager=auth_manager)

# ---------------------------
# Starlette app
# ---------------------------
routes = [
    Route("/login", login, methods=["POST"]),
    Route("/protected", protected, methods=["GET"]),
    WebSocketRoute("/ws", ChatWebSocket()),
]

app = Starlette(routes=routes)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```
## other example using example and microframe 

### install
```bash
    pip install git+https://github.com/traoreera/microframe.git
```
```python
from microframe import AppConfig, Application
from examples.authWs import router, ChatWebSocket # this module is not auto-install go to git to copy this 
from starlette.routing import WebSocketRoute
app = Application(
    AppConfig(
        title="MicroFrame",
        version="2.0.0",
        description="A modern ASGI microframe",
        debug=True,
    )
)


app = Application(configuration=AppConfig("AuthX", "1.0.0"))

@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocketRoute):
    await websocket.accept()
    
    if user_id:= await ChatWebSocket().authenticate(websocket):
    
        await ChatWebSocket().on_connect(websocket, f"{user_id}")
        rsp = await ChatWebSocket().on_receive(websocket)

        await ChatWebSocket().on_message(websocket, f"{user_id}", f"{rsp.get('text')}")
        await ChatWebSocket().on_disconnect(websocket, f"{user_id}")
    await websocket.close()
app.include_router(router)

```
# run app
```bash
uvicorn main:app --reload 
```




---

### 🔹 Flow

1. **Login**

```bash
POST /login
{
  "username": "user@example.com",
  "passwrd": "password123"
}
```

Response:

```json
{
  "accessToken": "...jwt access token...",
  "refreshToken": "...jwt refresh token...",
  "tokenType": "bearer"
}
```

2. **Protected API**

```http
GET /protected
Authorization: Bearer <access_token>
```

Response:

```json
{
  "message": "Hello user@example.com!"
}
```

3. **WebSocket Connection**

```javascript
// Example using browser JS
const token = "<access_token>";
const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

ws.onmessage = (event) => console.log(event.data);
ws.onopen = () => ws.send(JSON.stringify({ text: "Hello WebSocket!" }));
```

Response:

```json
{
  "user": "42",
  "message": { "text": "Hello WebSocket!" }
}
```

---

This example demonstrates:

* JWT login & token issuance
* Protecting API endpoints
* Authenticated WebSocket connections with `BaseWebSocket`
* Sending and receiving messages in real-time
