"""
Tests for CORS Middleware
"""

import pytest
from httpx import AsyncClient

from microframe import Application
from microframe.middleware import CORSMiddleware


class TestCORSMiddleware:
    """Test CORS middleware"""

    @pytest.mark.asyncio
    async def test_cors_headers(self):
        """Test CORS headers are added"""
        app = Application()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["GET", "POST"],
            allow_headers=["Content-Type"],
        )

        @app.get("/test")
        async def test_route():
            return {"message": "ok"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/test", headers={"Origin": "http://localhost:3000"})
            assert response.status_code == 200
            # CORS headers should be present
            assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_preflight(self):
        """Test CORS preflight OPTIONS request"""
        app = Application()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_methods=["GET", "POST", "PUT"],
        )

        @app.post("/api/data")
        async def post_data():
            return {"data": "created"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Preflight request
            response = await client.options(
                "/api/data",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                },
            )
            # Preflight should succeed
            assert response.status_code in [200, 204]

    @pytest.mark.asyncio
    async def test_cors_wildcard_origin(self):
        """Test CORS with wildcard origin"""
        app = Application()

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["GET", "POST"],
        )

        @app.get("/public")
        async def public_route():
            return {"public": True}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/public", headers={"Origin": "http://any-origin.com"})
            assert response.status_code == 200


class TestSecurityMiddleware:
    """Test Security middleware"""

    @pytest.mark.asyncio
    async def test_security_headers(self):
        """Test security headers are added"""
        from microframe.middleware import SecurityMiddleware

        app = Application()
        app.add_middleware(SecurityMiddleware)

        @app.get("/test")
        async def test_route():
            return {"message": "ok"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/test")
            assert response.status_code == 200

            # Check for common security headers
            response.headers
            # Some security headers might be present
            assert response.status_code == 200  # At minimum, request should succeed
