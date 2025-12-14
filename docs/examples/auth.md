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
    create_auth_router,
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

    async def authenticate(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if user.get("password") == password:
            return user
        return None


# Dependency Injection
app.state.auth_manager = InMemoryAuthManager()
app.state.auth_config = auth_config

# Include auth router
auth_router = create_auth_router()
app.include_router(auth_router)

# Public route
@app.get("/")
async def public_route():
    return {"message": "This route is public."}

# Protected route
@app.get("/protected", response_model=UserResponse)
async def protected_route(current_user: UserResponse = Depends(get_current_user)):
    return current_user
