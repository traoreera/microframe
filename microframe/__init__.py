"""
MicroFrame - A modern ASGI microframe

Example:
```python
    from microframe import Application, Router, AppConfig
    from microframe.dependencies import Depends
    
    app = Application(title="My API", version="1.0.0")
    
    @app.get("/")
    async def index():
        return {"message": "Hello World"}
```
"""

import typing

if typing.TYPE_CHECKING:
    from starlette import status
    from starlette.requests import Request

    from microframe.core import (
        AppConfig,
        Application,
        ForbiddenException,
        HTTPException,
        MicroFrameException,
        NotFoundException,
        UnauthorizedException,
        ValidationException,
    )
    from microframe.dependencies import Depends
    from microframe.middleware import CORSMiddleware, SecurityMiddleware
    from microframe.routing import Router

__version__ = "2.0.0"

_import_map = {
    "Application": "microframe.core",
    "AppConfig": "microframe.core",
    "Router": "microframe.routing",
    "Depends": "microframe.dependencies",
    "CORSMiddleware": "microframe.middleware",
    "SecurityMiddleware": "microframe.middleware",
    "MicroFrameException": "microframe.core",
    "HTTPException": "microframe.core",
    "ValidationException": "microframe.core",
    "NotFoundException": "microframe.core",
    "UnauthorizedException": "microframe.core",
    "ForbiddenException": "microframe.core",
    "Request": "starlette.requests",
    "status": "starlette",
}

__all__ = list(_import_map.keys())


def __getattr__(name: str):
    if name in _import_map:
        module_path = _import_map[name]
        import importlib

        module = importlib.import_module(module_path)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
