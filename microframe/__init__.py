"""
MicroFramework - A modern ASGI microframework

Example:
    from microframe import Application, Router
    from microframe.dependencies import Depends
    
    app = Application(title="My API", version="1.0.0")
    
    @app.get("/")
    async def index():
        return {"message": "Hello World"}
"""

__version__ = "2.0.0"

from .core import (
    Application,
    AppConfig,
    MicroFrameException,
    HTTPException,
    ValidationException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)
from .routing import Router
from .dependencies import Depends
from .middleware import CORSMiddleware, SecurityMiddleware

__all__ = [
    "Application",
    "AppConfig",
    "Router",
    "Depends",
    "CORSMiddleware",
    "SecurityMiddleware",
    "MicroFrameException",
    "HTTPException",
    "ValidationException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException"
]