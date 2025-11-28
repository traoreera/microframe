"""
pytest configuration and shared fixtures
"""

import pytest
from httpx import AsyncClient

from microframe import AppConfig, Application


@pytest.fixture
def app_config():
    """Fixture for application configuration"""
    return AppConfig(
        title="Test API",
        version="1.0.0",
        description="Test Application",
        debug=True,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )


@pytest.fixture
def app(app_config):
    """Fixture for basic application"""
    return Application(configuration=app_config)


@pytest.fixture
async def client(app):
    """Fixture for async HTTP client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_routes():
    """Fixture for sample routes data"""
    return {
        "routes": [
            {"path": "/", "methods": ["GET"]},
            {"path": "/users", "methods": ["GET", "POST"]},
            {"path": "/users/{user_id}", "methods": ["GET", "PUT", "DELETE"]},
        ]
    }
