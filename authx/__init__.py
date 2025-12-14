"""

# **AuthX — JWT Authentication for Starlette**

AuthX is a modular JWT authentication system tailored for Starlette and compatible with any ASGI framework (microframe https://github.com/traoreera/microframe). It brings a clean and extensible architecture to secure APIs with strong authentication practices.

---

## **Core Capabilities**

### 🔹 Authentication Service

Robust JWT-based authentication with support for:

* Access & Refresh token workflows
* Configurable expiration policies
* Token rotation and optional blacklist strategies
* Signature algorithms (HS256, RS256, ES256, etc.)

### 🔹 Dependency Injection

AuthX works seamlessly with Starlette’s dependency system.
Inject your authentication backend, token provider, or user resolver without modifying your route logic.

### 🔹 Exception Handling

Includes built-in exceptions and handlers for common authentication failures:

* Invalid token
* Expired token
* Missing credentials
* Permission denied

Errors are standardized and can be overridden or extended.

---

## **Architecture Highlights**

* **Extensible:** Override any layer — token generation, storage, user identity, or permissions.
* **Framework-agnostic:** Works natively with Starlette; FastAPI, Litestar, or custom ASGI stacks require minimal adaptation.
* **Secure by design:** Protects against replay attacks, tampering, and CSRF (optional cookie+header mode).
* **Scalable:** Stateless architecture makes it suitable for distributed environments and horizontal scaling.
* **High performance:** Lightweight, minimal overhead, optimized async workflow.
---

## **Development & Maintenance Benefits**

* **Reusable across services**
* **Easy to test (mockable services, pure async interfaces)**
* **Backward and forward compatible**
* **Standards-compliant (JWT RFC 7519)**

---

## **Use Cases**

* REST APIs
* Microservices authentication
* Multi-tenant or modular systems
* IoT/embedded ASGI gateways
* Dashboard or SPA backend authentication

---

## **Example Usage**

```python
# Imports for AuthX
from authx import AuthConfig, AuthManager, create_access_token, create_refresh_token, decode_token
from authx.exceptions import CredentialsException
from authx.models import LoginRequest, TokenResponse

# ASGI
from microframe import AppConfig, Application, Request

# Configuration
auth_config = AuthConfig(
    secret_key="votre-cle-secrete-min-32-caracteres",
)

app_config = AppConfig(
    title="AuthX",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True,
)

# ASGI app
app = Application(configuration=app_config)


# your custom db

class MyDb(AuthManager):

    fake_db = {
        "hunters@gmail.com": {
            "id": "12",
            "email": "hunters@gmail.com",
            "password": "password",
        },
        "admin@gmail.com": {
            "id": "12",
            "email": "admin@gmail.com",
            "password": "password",
        },
    }

    def get_user_by_email(self, email: str):

        return self.fake_db.get(email, None)

    def get_user_by_id(self, user_id: int):

        return self.fake_db.get(user_id, None)

    def verify_password(self, email: str, password: str) -> bool:

        user = self.get_user_by_email(email)
        if not user:
            return False, None
        if user.get("password") == password:
            return True, user

        return False

    async def authenticate(self, email: str, password: str):

        acess, user = self.verify_password(email, password)
        if not acess:
            return None
        return user


# Dependency Injection
app.state.auth_manager = MyDb()
app.state.auth_config = auth_config


@app.post(
    "/login",
)
async def login(request: Request, user: LoginRequest):
    manager = app.state.auth_manager
    if response := await manager.authenticate(user.email, user.password):
        refreche_token = create_refresh_token(response.get("id"), auth_config)
        access_token = create_access_token(response.get("id"), auth_config)

        return TokenResponse(access_token=access_token, refresh_token=refreche_token).response_model
    else:
        return CredentialsException("user not found").__dict__

```

---

## **Summary**

AuthX is engineered for real-world production workloads — simple to integrate, easy to extend, and optimized for security and performance. It brings flexibility without sacrificing rigor, making it suitable for small projects up to distributed enterprise architectures.

"""

__version__ = "0.1.0"

from authx.config import AuthConfig
from authx.dependencies import get_current_user
from authx.exceptions import (
    AuthException,
    CredentialsException,
    InvalidTokenException,
    TokenExpiredException,
    UserNotFoundException,
)
from authx.jwt import create_access_token, create_refresh_token, create_token, decode_token
from authx.manager import AuthManager
from authx.models import LoginRequest, TokenResponse, UserResponse
from authx.security import hash_password, verify_password

from authx.routes import create_auth_router

from authx.middleware import AuthMiddleware

__all__ = [
    "AuthConfig",
    "AuthManager",
    "get_current_user",
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "AuthException",
    "CredentialsException",
    "InvalidTokenException",
    "TokenExpiredException",
    "UserNotFoundException",
    "verify_password",
    "hash_password",
    "create_access_token",
    "create_refresh_token",
    "create_token",
    "decode_token",
    "create_auth_router",
    "AuthMiddleware",
]
