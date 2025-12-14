# AuthX for MicroFrame

Modular and reusable JWT authentication module for MicroFrame.

## Installation

This module is already included in MicroFrame.

## Quick Start

Here is a quick example of how to use the authentication module in a MicroFrame application.

```python
from microframe import (
    Application,
    AppConfig,
    Request,
    Router,
    AuthManager,
    AuthConfig,
    Depends,
    get_current_user,
    UserResponse,
    auth_router,
    AuthMiddleware,
)

# Configuration
auth_config = AuthConfig(
    secret_key="your-secret-key-of-at-least-32-characters",
)

app_config = AppConfig(
    title="AuthX Example",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=True,
)

# ASGI app
app = Application(configuration=app_config)
app.add_middleware(AuthMiddleware, allow_unsecure=["/docs", "/redoc", "/openapi.json", "/", "/auth/login"])

# In-memory user database
class InMemoryAuthManager(AuthManager):
    fake_db = {
        "user@example.com": {
            "id": "1",
            "email": "user@example.com",
            "password": "password",
        },
    }

    async def get_user_by_email(self, email: str):
        return self.fake_db.get(email)

    async def get_user_by_id(self, user_id: str):
        for user in self.fake_db.values():
            if user["id"] == user_id:
                return user
        return None

    async def verify_password(self, email: str, password: str) -> tuple[bool, dict | None]:
        user = await self.get_user_by_email(email)
        if not user:
            return False, None
        if user.get("password") == password:
            return True, user
        return False, None

    async def authenticate(self, email: str, password: str):
        verified, user = await self.verify_password(email, password)
        if not verified:
            return None
        return user


# Dependency Injection
app.state.auth_manager = InMemoryAuthManager()
app.state.auth_config = auth_config

# Include auth router
app.include_router(auth_router)

# Public route
@app.get("/")
async def public_route():
    return {"message": "This route is public."}

# Protected route
@app.get("/protected", response_model=UserResponse)
async def protected_route(current_user: UserResponse = Depends(get_current_user)):
    return current_user

```


## Protected Routes





To protect a route, you can use the `get_current_user` dependency.





```python


from microframe import Depends, get_current_user, UserResponse





@app.get("/protected", response_model=UserResponse)


async def protected_route(current_user: UserResponse = Depends(get_current_user)):


    return current_user


```





## Advanced Configuration





You can configure the authentication module by passing an `AuthConfig` object to the application state.





```python


from microframe import AuthConfig





auth_config = AuthConfig(


    secret_key="your-secret-key-of-at-least-32-characters",


    algorithm="HS256",  # or "RS256"


    access_token_expire_minutes=15,


    refresh_token_expire_days=7,


    cookie_name="refresh_token",


    cookie_secure=True,  # Enable in production with HTTPS


    cookie_httponly=True,


    cookie_samesite="strict",  # "strict", "lax", or "none"


)





app.state.auth_config = auth_config


```





## Production Security





### Environment Variables





It is recommended to use environment variables for sensitive data.





```bash


# .env


SECRET_KEY=generate-with-openssl-rand-hex-32


COOKIE_SECURE=true


ACCESS_TOKEN_EXPIRE_MINUTES=15


REFRESH_TOKEN_EXPIRE_DAYS=7


```





### Generating a Secret Key





```bash


# With OpenSSL


openssl rand -hex 32





# With Python


python -c "import secrets; print(secrets.token_hex(32))"


```





### Production Checklist





- ✅ `SECRET_KEY` long and random (min 32 characters)


- ✅ `COOKIE_SECURE=true` (requires HTTPS)


- ✅ `cookie_samesite="strict"`


- ✅ CORS configured correctly (`allowed_origins`)


- ✅ Persistent database (not in-memory)


- ✅ HTTPS enabled


- ✅ Rate limiting on `/auth/login`





## Module Architecture





```


authx/


├── __init__.py          # Public exports


├── config.py            # AuthConfig configuration


├── jwt.py               # JWT creation/validation


├── models.py            # Pydantic models


├── manager.py           # Abstract AuthManager


├── dependencies.py      # `get_current_user` dependency


├── security.py          # Password hashing/verification


├── exceptions.py        # Custom exceptions


├── routes.py            # Authentication routes


└── middleware.py        # Authentication middleware


```





## Development





### Running the example





```bash


cd examples


python auth_example.py


```





## License





MIT

