from starlette.responses import RedirectResponse
from starlette.routing import WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket

from examples.protected import AuthConfig, MyDb
from examples.protected import router as protected
from examples.template_testing import router
from microframe import AppConfig, Application, Depends, status
from starthub.routes import router as starthub_router

app = Application(
    AppConfig(
        title="MicroFrame",
        version="2.0.0",
        description="A modern ASGI microframe",
        debug=True,
    )
)


app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/", status_code=status.HTTP_200_OK)
def index(curent_user=Depends):
    return RedirectResponse(url="/starthub")


app.state.auth_manager = MyDb()
app.state.auth_config = AuthConfig(secret_key="jherjgernjikn")


def ws_handler(websocket: WebSocket):
    print(websocket.accept())

    return WebSocket(scope=websocket.scope, receive=websocket.receive, send=websocket.send)


app.include_router(router, tags=["Demo UI"])
app.include_router(starthub_router, tags=["Starthub"])
app.include_router(protected, tags=["Protected"])
