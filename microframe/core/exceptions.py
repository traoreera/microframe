"""
Core exceptions for the microframework
"""

from typing import Any, Dict, Optional


class MicroFrameException(Exception):
    """Base exception for all framework exceptions"""

    def __init__(
        self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {"message": self.message, "status_code": self.status_code, "details": self.details}


class HTTPException(MicroFrameException):
    """HTTP specific exception"""



class ValidationException(MicroFrameException):
    """Validation error exception"""

    def __init__(self, message: str = "Validation error", errors: list = None):
        super().__init__(message=message, status_code=422, details={"errors": errors or []})

    def __call__(self, request: Any) -> dict:
        return self.to_dict()


class DependencyException(MicroFrameException):
    """Dependency resolution exception"""

    def __init__(self, message: str):
        super().__init__(message, status_code=500)

    def __call__(self, request: Any) -> dict:
        return self.to_dict()


class NotFoundException(HTTPException):
    """Resource not found exception"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

    def __call__(self, request: Any) -> dict:
        return self.to_dict()


class UnauthorizedException(HTTPException):
    """Unauthorized access exception"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)

    def __call__(self, request: Any) -> dict:
        return self.to_dict()


class ForbiddenException(HTTPException):
    """Forbidden access exception"""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)

    def __call__(self, request: Any) -> dict:
        return self.to_dict()
