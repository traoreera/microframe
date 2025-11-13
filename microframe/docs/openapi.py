"""
OpenAPI schema generation
"""

import inspect
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel

from ..core.config import AppConfig
from ..routing.models import RouteInfo


class OpenAPIGenerator:
    """Generate OpenAPI 3.0 schema"""

    def __init__(self, routes: list[RouteInfo], title: str, version: str, description: str):
        self.routes = routes
        self.title = title
        self.version = version
        self.description = description

    def generate(
        self,
    ) -> Dict[str, Any]:
        """
        Generate complete OpenAPI schema

        Args:
            routes: List of route information

        Returns:
            OpenAPI schema dictionary
        """
        paths = {}

        for route_info in self.routes:
            if not route_info.include_in_schema:
                continue

            path_item = paths.get(route_info.path, {})

            for k, v in path_item.items():
                if v in ["db", "settings"]:
                    path_item[k].pop

            for method in route_info.methods:
                method_lower = method.lower()
                path_item[method_lower] = self._generate_operation(route_info)

            paths[route_info.path] = path_item

        return {
            "openapi": "3.0.2",
            "info": {"title": self.title, "version": self.version, "description": self.description},
            "paths": paths,
        }

    def _generate_operation(self, route_info: RouteInfo) -> Dict[str, Any]:
        """Generate operation object for a route"""
        parameters, request_body = self._extract_parameters(route_info.func)

        operation = {
            "summary": route_info.summary,
            "description": route_info.description or "",
            "tags": route_info.tags,
            "operationId": route_info.func.__name__,
            "responses": {
                str(route_info.status_code): {
                    "description": "Successful Response",
                },
                "422": {"description": "Validation Error"},
            },
        }

        if parameters:
            operation["parameters"] = parameters

        if request_body:
            operation["requestBody"] = request_body

        if route_info.deprecated:
            operation["deprecated"] = True

        return operation

    def _extract_parameters(
        self, func: callable  # type: ignore
    ) -> Tuple[List[Dict], Dict[Any, Any]]:
        """Extract parameters and request body from function signature"""
        sig = inspect.signature(func)
        parameters = []
        request_body = None

        for param_name, param in sig.parameters.items():
            if param_name in [
                "request",
                "self",
                "db",
                "curent_user",
                "curent_admin",
                "curent_superuser",
                "settings",
            ]:
                continue

            annotation = param.annotation

            # Pydantic model = request body
            if self._is_pydantic_model(annotation):
                request_body = {
                    "required": True,
                    "content": {"application/json": {"schema": annotation.model_json_schema()}},
                }

            # Other parameters = query parameters
            else:
                param_schema = self._get_param_schema(annotation)
                parameters.append(
                    {
                        "name": param_name,
                        "in": "query",
                        "required": param.default == inspect.Parameter.empty,
                        "schema": param_schema,
                    }
                )

        return parameters, request_body

    @staticmethod
    def _is_pydantic_model(cls) -> bool:
        """Check if class is Pydantic model"""
        try:
            return isinstance(cls, type) and issubclass(cls, BaseModel)
        except TypeError:
            return False

    @staticmethod
    def _get_param_schema(annotation) -> Dict[str, str]:
        """Get JSON schema for parameter type"""
        type_map = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        return {"type": type_map.get(annotation, "string")}
