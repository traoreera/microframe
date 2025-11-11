from microframe import Depends
from microframe.app import Application
from microframe.routing import Router as APIRouter
from websockets import Request

from ecommerce.routes.items import router as items_router

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = Application(
    title="Test Swagger",
    version="1.0.0",
    description="Application de test pour vérifier Swagger UI"
)

ecommerce = APIRouter(prefix="/v1/ecommerce", tags=["ecommerce", "api"])
test = APIRouter(prefix="/v1/test", tags=["test"])


@test.get("/ping", summary="Ping the server", response_model=str, tags=["test"], status_code=200)
def ping(request: Request, ) -> str:
    """Endpoint to check if the server is alive."""


    return "pong"

@test.get("/items", summary="Get an item by ID", response_model=str, tags=["test"], status_code=200)
def get_item(request: Request, item: Item) -> str:
    """Endpoint to get an item by ID."""

    return f"Item received: {item.name}"


def get_database():
    return {"type": "postgres", "connected": True}


@app.post("/data")
async def get_data(user_agent,db=Depends(get_database)):
    print(user_agent)
    return {"data": "...", "database": db}

ecommerce.include_router(items_router, prefix=ecommerce.prefix, tags=ecommerce.tags)
app.include_router(ecommerce )
app.include_router(test)


