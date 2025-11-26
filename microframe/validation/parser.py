"""
Request parameter parsing and validation
"""

import inspect
import logging
from typing import Any, Callable, Dict

from pydantic import BaseModel, ValidationError
from starlette.requests import Request

from ..dependencies.exceptionHandler import Depends
from ..exceptions.exception import ValidationException

logger = logging.getLogger(__name__)


class RequestParser:
    """Parse and validate request parameters"""

    async def parse(self, request: Request, func: Callable) -> Dict[str, Any]:
        """
        Parse request and extract parameters for function

        Args:
            request: Starlette request object
            func: Handler function

        Returns:
            Dictionary of parsed parameters
        """
        sig = inspect.signature(func)
        params = {}

        # Parse query parameters
        query_params = dict(request.query_params)

        # Parse path parameters
        path_params = dict(request.path_params)

        # Parse body if applicable
        body_data = {}
        if request.method in ["POST", "PUT", "PATCH"]:
            body_data = await self._parse_body(request)

        # Match parameters to function signature
        for param_name, param in sig.parameters.items():
            # Skip special parameters
            if param_name in ["request", "self"]:
                if param_name == "request":
                    params[param_name] = request
                continue

            # skip depends
            if isinstance(param.default, Depends):
                continue

            annotation = param.annotation

            # Pydantic model - validate body
            if self._is_pydantic_model(annotation):
                try:
                    params[param_name] = annotation(**body_data)
                except ValidationError as e:
                    return ValidationException(
                        message="Request validation failed", errors=e.errors()
                    ).to_dict()

            # Path parameter
            elif param_name in path_params:
                params[param_name] = path_params[param_name]

            # Query parameter
            elif param_name in query_params:
                params[param_name] = query_params[param_name]

            # Default value
            elif param.default != inspect.Parameter.empty:
                params[param_name] = param.default

        return params

    async def _parse_body(self, request: Request) -> Dict[str, Any]:
        """Parse request body"""
        try:
            content_type = request.headers.get("content-type", "")

            if "application/json" in content_type:
                return await request.json()
            elif "application/x-www-form-urlencoded" in content_type:
                form = await request.form()
                return dict(form)
            else:
                return {}

        except Exception as e:
            logger.error(f"Error parsing request body: {e}")
            raise ValidationException(message="Invalid request body", errors=[{"msg": str(e)}])

    @staticmethod
    def _is_pydantic_model(cls) -> bool:
        """Check if class is a Pydantic model"""
        try:
            return isinstance(cls, type) and issubclass(cls, BaseModel)
        except TypeError:
            return False
