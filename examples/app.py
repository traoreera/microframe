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
