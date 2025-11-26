"""
Tests for Router functionality
"""

import pytest
from httpx import AsyncClient

from microframe import Application, Router


class TestRouter:
    """Test Router class"""

    def test_router_initialization(self):
        """Test router initializes with config"""
        router = Router(prefix="/api", tags=["API"])
        assert router.prefix == "/api"
        assert router.tags == ["API"]

    def test_router_add_route(self):
        """Test adding route to router"""
        router = Router(prefix="/users")

        @router.get("/")
        async def list_users():
            return {"users": []}

        routes = router.get_routes()
        assert len(routes) == 1
        assert routes[0].path == "/users/"
        assert routes[0].methods == ["GET"]

    @pytest.mark.asyncio
    async def test_router_get_decorator(self):
        """Test GET route decorator"""
        app = Application()
        router = Router(prefix="/items")

        @router.get("/")
        async def list_items():
            return {"items": ["item1", "item2"]}

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/items/")
            assert response.status_code == 200
            assert response.json() == {"items": ["item1", "item2"]}

    @pytest.mark.asyncio
    async def test_router_post_decorator(self):
        """Test POST route decorator"""
        app = Application()
        router = Router(prefix="/items")

        @router.post("/")
        async def create_item():
            return {"created": True}

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/items/")
            assert response.status_code == 200
            assert response.json() == {"created": True}

    @pytest.mark.asyncio
    async def test_nested_routers(self):
        """Test nested router inclusion"""
        app = Application()

        # Main API router
        api_router = Router(prefix="/api")

        users_router = Router(prefix="/users", tags=["Users"])
        posts_router = Router(prefix="/posts", tags=["Posts"])

        @users_router.get("/")
        async def list_users():
            return {"users": []}

        @users_router.get("/{user_id}")
        async def get_user(user_id: str):
            return {"user_id": user_id}

            # Posts sub-router

        @posts_router.get("/")
        async def list_posts():
            return {"posts": []}

            # Include sub-routers

        api_router.include_router(users_router)
        api_router.include_router(posts_router)

        app.include_router(api_router, "/api")

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Test users routes
            response = await client.get("/api/users/")
            assert response.status_code == 200
            assert response.json() == {"users": []}

            response = await client.get("/api/users/123")
            assert response.status_code == 200
            assert response.json() == {"user_id": "123"}

            # Test posts routes
            response = await client.get("/api/posts/")
            assert response.status_code == 200
            assert response.json() == {"posts": []}

    def test_router_tags_merging(self):
        """Test that tags are properly merged"""
        router = Router(prefix="/api", tags=["API"])

        @router.get("/test", tags=["Test"])
        async def test_route():
            return {}

        routes = router.get_routes()
        assert len(routes) == 1
        assert "API" in routes[0].tags
        assert "Test" in routes[0].tags

    def test_router_all_http_methods(self):
        """Test all HTTP method decorators on router"""
        router = Router(prefix="/test")

        @router.get("/get")
        async def get_route():
            return {"method": "GET"}

        @router.post("/post")
        async def post_route():
            return {"method": "POST"}

        @router.put("/put")
        async def put_route():
            return {"method": "PUT"}

        @router.patch("/patch")
        async def patch_route():
            return {"method": "PATCH"}

        @router.delete("/delete")
        async def delete_route():
            return {"method": "DELETE"}

        routes = router.get_routes()
        assert len(routes) == 5

    @pytest.mark.asyncio
    async def test_router_path_parameters(self):
        """Test router with path parameters"""
        app = Application()
        router = Router(prefix="/users")

        @router.get("/{user_id}/posts/{post_id}")
        async def get_user_post(user_id: str, post_id: str):
            return {"user_id": user_id, "post_id": post_id}

        app.include_router(router)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/users/123/posts/456")
            assert response.status_code == 200
            assert response.json() == {"user_id": "123", "post_id": "456"}

    def test_router_prefix_normalization(self):
        """Test that router prefix is normalized"""
        router1 = Router(prefix="/api/")
        router2 = Router(prefix="/api")

        # Both should normalize to same prefix
        assert router1.prefix == "/api"
        assert router2.prefix == "/api"

    def test_router_get_routes_with_prefix(self):
        """Test getting routes with additional prefix"""
        router = Router(prefix="/users")

        @router.get("/")
        async def list_users():
            return {}

        routes = router.get_routes(prefix="/api")
        assert len(routes) == 1
        assert routes[0].path == "/api/users/"
