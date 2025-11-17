from datetime import timedelta
from typing import Any, Dict, List, Optional

from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class CookieResponse:
    """
    Gestionnaire avancé de cookies + réponse HTTP.
    - Chaînable
    - Sécurisé par défaut
    - Compatible Microframe / FastAPI / Starlette
    """

    __slots__ = ["_cookies", "_delete_queue"]

    def __init__(self):
        self._cookies: List[Dict[str, Any]] = []
        self._delete_queue: List[str] = []

    # --- ==========================  COOKIE OPS  ========================== ---

    def set_cookie(
        self,
        name: str,
        value: Any,
        days: int = 7,
        secure: bool = True,
        http_only: bool = True,
        samesite: str = "strict",
        domain: Optional[str] = None,
        path: str = "/",
    ):
        """Enregistre un cookie sécurisé avec expiration."""

        self._cookies.append(
            {
                "key": name,
                "value": str(value),
                "max_age": int(timedelta(days=days).total_seconds()),
                "httponly": http_only,
                "path": path,
                "secure": secure,
                "samesite": samesite,
                "domain": domain,
            }
        )
        return self

    def delete_cookie(self, name: str, path: str = "/", domain: Optional[str] = None):
        """Marque un cookie pour suppression (RFC compliant)."""
        self._delete_queue.append(name)
        self._cookies.append(
            {"key": name, "value": "", "max_age": 0, "expires": 0, "path": path, "domain": domain}
        )
        return self

    # --- ==========================  RESPONSE  ========================== ---

    def json(
        self,
        content: Dict[str, Any],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ) -> JSONResponse:
        """Construit la réponse JSON avec tous les cookies appliqués."""
        response = JSONResponse(content, status_code=status_code, headers=headers)
        self._apply_cookies(response)
        return response

    def response(
        self, body: str = "", status: int = 200, headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """Alternative non-JSON."""
        response = Response(body, status_code=status, headers=headers)
        self._apply_cookies(response)
        return response

    # --- ==========================  REQUEST Helpers ====================== ---

    @staticmethod
    def get_cookie(request: Request, name: str, default: Optional[str] = None):
        """Récupère un cookie dans la requête."""
        return request.cookies.get(name, default)

    @staticmethod
    def has_cookie(request: Request, name: str) -> bool:
        """Vérifie présence cookie."""
        return name in request.cookies

    # --- ==========================  Internals ============================ ---

    def _apply_cookies(self, response: Response):
        """Finalisation: push tous les cookies dans la réponse HTTP."""
        for cookie in self._cookies:
            response.set_cookie(**cookie)


def get_cookie_response() -> CookieResponse:
    """Factory compatible Microframe/Starlette/FastAPI Depends()."""
    return CookieResponse()
