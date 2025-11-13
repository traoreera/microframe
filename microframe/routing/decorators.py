"""
Route decorators
"""

from typing import Callable, List

from .models import RouteInfo


def route_decorator(path: str, func: Callable, methods: List[str], **kwargs) -> RouteInfo:
    """Create a RouteInfo from decorator parameters"""
    return RouteInfo(path=path, func=func, methods=methods, **kwargs)
