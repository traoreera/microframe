from datetime import datetime
from typing import Any, Dict, List, Optional

from starlette.exceptions import HTTPException as StarletteHTTPException


class BaseExceptionPayload:
    """Serializable error payload"""

    def __init__(
        self,
        message: str,
        status_code: int,
        errors: Optional[List[Any]] = None,
        code: Optional[str] = None,
        debug: bool = False,
    ):

        self.timestamp = datetime.utcnow().isoformat()
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        self.code = code

        # Only expose details in debug mode
        self.debug = debug

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "status": self.status_code,
            "timestamp": self.timestamp,
        }

        if self.errors:
            payload["errors"] = self.errors

        if self.code:
            payload["code"] = self.code

        if self.debug:
            payload["debug"] = True

        return payload


class MicroFrameException(Exception):
    """Base exception for application-level errors (non HTTP specific)."""

    def __init__(
        self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None
    ):
        self.payload = BaseExceptionPayload(
            message=message,
            status_code=status_code,
            errors=details.get("errors") if details else None,
        )
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        return self.payload.to_dict()


class HTTPException(StarletteHTTPException):
    """Unified HTTP exception with automatic response formatting."""

    def __init__(
        self,
        status_code: int,
        detail: str = None,
        errors: Optional[List[Any]] = None,
        code: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.payload = BaseExceptionPayload(
            message=detail or "HTTP Error",
            status_code=status_code,
            errors=errors,
            code=code,
        )

    def to_dict(self):
        return self.payload.to_dict()


# === Specific Framework Exceptions ===============================


class NotFoundException(HTTPException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(404, detail=message, code="NOT_FOUND")


class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(401, detail=message, code="UNAUTHORIZED")


class ForbiddenException(HTTPException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(403, detail=message, code="FORBIDDEN")


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(400, detail=message, code="BAD_REQUEST")


class ValidationException(HTTPException):
    def __init__(self, message: str = "Validation error", errors: Optional[List[Any]] = None):
        super().__init__(422, detail=message, errors=errors, code="VALIDATION_ERROR")
