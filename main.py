from typing import Any, Optional

from starlette.middleware.sessions import SessionMiddleware

from authx import (
    AuthConfig,
    AuthManager,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from authx.models import LoginRequest, TokenResponse
from microframe import AppConfig, Application, Depends, NotFoundException, Request
from microui.auth_pages import AuthPages

appConf = AppConfig(title="DaisyUI Kit", version="0.0.1", debug=True)

app = Application(configuration=appConf)


auth_page = AuthPages()

auth_configure = AuthConfig(
    secret_key="mysecretkey",
    algorithm="HS256",
    access_token_expire_minutes=30,
    refresh_token_expire_days=7,
)


class Manager(AuthManager):

    def verified_user(self, user: LoginRequest) -> Optional[dict | Any]:
        if user.email == "admin@gmail.com" and user.password == "admin123":
            return {"email": user.email}
        else:
            raise NotFoundException("Invalid credentials")


app.state.auth_manager = Manager()
app.state.auth_configure = auth_configure


@app.post("/login", response_model=TokenResponse)
def login(request: Request, credentials: LoginRequest):

    if credentials.email == "admin@gmail.com" and credentials.password == "admin123":
        access_token = create_access_token(credentials.email, auth_configure)
        refresh_token = create_refresh_token(credentials.email, auth_configure)

        user = request.session

        user["user"] = {"access_token": access_token, "refresh_token": refresh_token}

        request.session.update(user)

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    else:
        raise NotFoundException("Invalid credentials")


@app.get(
    "/me",
)
async def me(request: Request, current_user=Depends(get_current_user)):

    return current_user


app.add_middleware(SessionMiddleware, secret_key="secret")
