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
    AppConfig,
    Application,
    ForbiddenException,
    HTTPException,
    MicroFrameException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
)
from .dependencies import Depends
from .middleware import CORSMiddleware, SecurityMiddleware
from .routing import Router

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
    "ForbiddenException",
]
