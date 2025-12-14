from datetime import datetime
from typing import Any, Dict, Optional

from starlette.exceptions import HTTPException


class AuthExceptionPayload:
    """Structure standardisée pour les erreurs d'authentification"""

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str,
        details: Optional[Dict[str, Any]] = None,
        debug: bool = False,
    ):

        self.message = message
        self.status = status_code
        self.error_code = error_code
        self.timestamp = datetime.utcnow().isoformat()
        self.details = details or {}
        self.debug = debug

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "error": self.error_code,
            "message": self.message,
            "status": self.status,
            "timestamp": self.timestamp,
        }

        if self.details:
            payload["details"] = self.details

        if self.debug:
            payload["debug"] = True

        return payload


class AuthException(HTTPException):
    """Base unifiée pour toutes les erreurs d’authentification"""

    error_code: str = "AUTH_ERROR"
    default_message: str = "Erreur d'authentification"
    status_code: int = 401

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        debug: bool = False,
    ):
        self.payload = AuthExceptionPayload(
            message=message or self.default_message,
            status_code=self.status_code,
            error_code=self.error_code,
            details=details,
            debug=debug,
        )

        super().__init__(status_code=self.status_code, detail=self.payload.message)

    @property
    def __dict__(self) -> Dict[str, Any]:
        """Return dictionary representation for JSON serialization."""
        return self.payload.to_dict()
    
    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation."""
        return self.payload.to_dict()


# === Exceptions spécialisées =============================


class CredentialsException(AuthException):
    error_code = "INVALID_CREDENTIALS"
    default_message = "Identifiants invalides"
    status_code = 401


class InvalidTokenException(AuthException):
    error_code = "INVALID_TOKEN"
    default_message = "Token invalide"
    status_code = 401


class TokenExpiredException(AuthException):
    error_code = "TOKEN_EXPIRED"
    default_message = "Token expiré"
    status_code = 401


class UserNotFoundException(AuthException):
    error_code = "USER_NOT_FOUND"
    default_message = "Utilisateur non trouvé"
    status_code = 404
