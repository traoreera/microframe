"""
Tests for Exception Handling
"""

import pytest
from httpx import AsyncClient

from microframe import Application
from microframe.exceptions.exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)


class TestExceptions:
    """Test exception handling"""

    @pytest.mark.asyncio
    async def test_not_found_exception(self):
        """Test NotFoundException returns 404"""
        from pydantic import BaseModel

        app = Application()

        class User(BaseModel):
            id: int

        @app.get("/users/{user_id}")
        async def get_user(user_id: int):
            if int(user_id) == 123:
                return {"user_id": user_id}
            raise NotFoundException(f"User not found")

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Valid user
            response = await client.get("/users/123")
            assert response.json()["user_id"] != 123

            response = await client.get("/users/999")
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_exception(self):
        """Test UnauthorizedException returns 401"""
        app = Application()

        @app.get("/protected")
        async def protected_route():
            raise UnauthorizedException("Authentication required")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/protected")
            assert response.status_code == 401
            assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_forbidden_exception(self):
        """Test ForbiddenException returns 403"""
        app = Application()

        @app.get("/admin")
        async def admin_route():
            raise ForbiddenException("Admin access required")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/admin")
            assert response.status_code == 403
            assert "error" in response.json()

    @pytest.mark.asyncio
    async def test_bad_request_exception(self):
        """Test BadRequestException returns 400"""
        app = Application()

        @app.post("/validate")
        async def validate_data():
            raise BadRequestException("Invalid data format")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/validate")
            assert response.status_code == 400
            assert "type" in response.json()

    @pytest.mark.asyncio
    async def test_generic_exception_handling(self):
        """Test generic exception handling"""
        app = Application()

        @app.get("/error")
        async def error_route():
            raise ValueError("Something went wrong")

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/error")
            # Should return 500 for unhandled exceptions
            assert response.status_code == 500

    @pytest.mark.asyncio
    async def test_route_not_found(self):
        """Test 404 for non-existent routes"""
        app = Application()

        @app.get("/exists")
        async def exists():
            return {"status": "ok"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Existing route
            response = await client.get("/exists")
            assert response.status_code == 200

            # Non-existent route
            response = await client.get("/does-not-exist")
            assert response.status_code == 404
