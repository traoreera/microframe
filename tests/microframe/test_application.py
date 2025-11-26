"""
Tests for Application core functionality
"""

import pytest
from httpx import AsyncClient
from pydantic import BaseModel

from microframe import Application, Router
from microframe.core import AppConfig


class TestApplication:
    """Test Application class"""

    def test_application_initialization(self, app_config):
        """Test app initializes with config"""
        app = Application(configuration=app_config)
        assert app.config.title == "Test API"
        assert app.config.version == "1.0.0"
        assert app.config.debug is True

    def test_application_default_config(self):
        """Test app with default config"""
        app = Application()
        assert app.config is not None
        assert isinstance(app.config, AppConfig)

    @pytest.mark.asyncio
    async def test_simple_route(self):
        """Test simple GET route"""
        app = Application()

        @app.get("/")
        async def index():
            return {"message": "Hello World"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

    @pytest.mark.asyncio
    async def test_path_parameter(self):
        """Test route with path parameter"""
        app = Application()

        @app.get("/users/{user_id}")
        async def get_user(user_id: str):
            return {"user_id": user_id}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/users/123")
            assert response.status_code == 200
            assert response.json() == {"user_id": "123"}

    @pytest.mark.asyncio
    async def test_post_request_with_body(self):
        """Test POST request with JSON body"""
        app = Application()

        class UserCreate(BaseModel):
            name: str
            email: str

        @app.post("/users")
        async def create_user(user: UserCreate):
            return {"name": user.name, "email": user.email}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/users", json={"name": "John", "email": "john@example.com"}
            )
            assert response.status_code == 200
            assert response.json() == {"name": "John", "email": "john@example.com"}

    @pytest.mark.asyncio
    async def test_multiple_http_methods(self):
        """Test same path with different methods"""
        app = Application()

        @app.get("/items")
        async def list_items():
            return {"items": []}

        @app.post("/items")
        async def create_item():
            return {"message": "created"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            get_response = await client.get("/items")
            assert get_response.status_code == 200
            assert get_response.json() == {"items": []}

            post_response = await client.post("/items")
            assert post_response.status_code == 200
            assert post_response.json() == {"message": "created"}

    @pytest.mark.asyncio
    async def test_include_router(self):
        """Test including a router"""
        app = Application()
        router = Router(prefix="/api", tags=["API"])

        @router.get("/health")
        async def health():
            return {"status": "ok"}

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    def test_route_decorator_methods(self):
        """Test all HTTP method decorators"""
        app = Application()

        @app.get("/get")
        async def get_route():
            return {"method": "GET"}

        @app.post("/post")
        async def post_route():
            return {"method": "POST"}

        @app.put("/put")
        async def put_route():
            return {"method": "PUT"}

        @app.patch("/patch")
        async def patch_route():
            return {"method": "PATCH"}

        @app.delete("/delete")
        async def delete_route():
            return {"method": "DELETE"}

        # Verify routes are registered
        assert len(app.routes) >= 5

    @pytest.mark.asyncio
    async def test_sync_handler(self):
        """Test synchronous handler function"""
        app = Application()

        @app.get("/sync")
        def sync_route():
            return {"sync": True}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/sync")
            assert response.status_code == 200
            assert response.json() == {"sync": True}
