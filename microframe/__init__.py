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

from starlette.requests import Request

from microframe.core.application import Application
from microframe.core.config import AppConfig
from microframe.dependencies.manager import DependencyManager, Depends
from microframe.exceptions.exception import *
from microframe.routing.router import RouteInfo, Router

__all__ = [
    "Application",
    "AppConfig",
    "Router",
    "RouteInfo",
    "Request",
    "DependencyManager",
    "Depends",
]
