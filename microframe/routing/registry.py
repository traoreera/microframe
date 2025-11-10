"""
Route registry for tracking all routes
"""
from typing import Dict, List, Optional

from .models import RouteInfo


class RouteRegistry:
    """Registry for tracking all application routes"""
    
    def __init__(self):
        self._routes: List[RouteInfo] = []
        self._by_path: Dict[str, List[RouteInfo]] = {}
        self._by_tag: Dict[str, List[RouteInfo]] = {}
    
    def register(self, route_info: RouteInfo):
        """Register a route"""
        self._routes.append(route_info)
        
        # Index by path
        if route_info.path not in self._by_path:
            self._by_path[route_info.path] = []
        self._by_path[route_info.path].append(route_info)
        
        # Index by tags
        for tag in route_info.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = []
            self._by_tag[tag].append(route_info)
    
    def get_all(self) -> List[RouteInfo]:
        """Get all registered routes"""
        return self._routes.copy()
    
    def get_by_path(self, path: str) -> List[RouteInfo]:
        """Get routes by path"""
        return self._by_path.get(path, [])
    
    def get_by_tag(self, tag: str) -> List[RouteInfo]:
        """Get routes by tag"""
        return self._by_tag.get(tag, [])
    
    def clear(self):
        """Clear all routes"""
        self._routes.clear()
        self._by_path.clear()
        self._by_tag.clear()
