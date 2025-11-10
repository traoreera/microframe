from microframe.app import Application
from microframe.security.jwt import get_current_user
from microframe.dependencies import Depends
from microframe.middleware import security
from microframe.routing import Router as APIRouter


app = Application(
    title="Test Swagger",
    version="1.0.0",
    description="Application de test pour vérifier Swagger UI"
)


test = APIRouter(prefix="/v1", tags=["Test Routes", "v1"])
tes2 = APIRouter(prefix="/test", tags=["Another Test Routes"])


test.get(path="/hello",)
def hello(request):
    """Route de salutation"""
    return {"message": "Hello, World!"}

@tes2.get(path="/ping",)
def ping(request):
    """Route de ping"""
    return {"message": "pong"}


test.include_router(tes2)


app.include_router(router=test)

#app.add_middleware(security.CORSMiddleware,allow_origins=["*"],)
#app.add_middleware(security.CORSMiddleware)
#print(app._generate_openapi())
