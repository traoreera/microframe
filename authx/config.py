"""
"""

from datetime import timedelta
from typing import Literal


class AuthConfig:
    """
    Core configuration object for the authentication system.

    This class centralizes all parameters required to control
    JWT generation, expiration policies, and cookie behavior.

    **Quick Start**

    ```python
    from authx.config import AuthConfig

    auth = AuthConfig(
        secret_key="your-very-long-secure-secret",
        algorithm="HS256",
    )
    ```

    **Parameters**
    ----------
    secret_key : str
        Secret used to sign and validate JWT tokens. Must be long, random,
        and never committed in source control.

    algorithm : Literal["HS256", "RS256"], optional
        JWT signing algorithm. Use:
        - `"HS256"` for symmetric HMAC signing (single shared secret).
        - `"RS256"` for asymmetric RSA key signing (public/private pair).
        Defaults to `"HS256"`.

    access_token_expire_minutes : int, optional
        Access token lifetime in minutes. Short-lived token enforcing frequent renewal.
        Defaults to `15`.

    refresh_token_expire_days : int, optional
        Refresh token lifetime in days. Long-term authentication persistence.
        Defaults to `7`.

    cookie_name : str, optional
        Name of the cookie storing the refresh token in secure deployments.
        Defaults to `"refresh_token"`.

    cookie_secure : bool, optional
        Forces cookie transmission exclusively over HTTPS.
        Enabled by default.

    cookie_httponly : bool, optional
        Prevents JavaScript access to authentication cookies, mitigating XSS impact.
        Enabled by default.

    cookie_samesite : Literal["strict", "lax", "none"], optional
        Controls cross-site cookie transmission behavior.
        Defaults to `"strict"`.

    **Attributes (computed)**
    ------------------------
    access_token_expire : timedelta
        Derived expiration duration for access tokens.

    refresh_token_expire : timedelta
        Derived expiration duration for refresh tokens.

    **Usage Notes**
    --------------
    - For production, always combine:
      - `HTTPS`
      - `cookie_secure=True`
      - `HTTPOnly cookies`
      - rotating refresh tokens

    - `RS256` mode is recommended for distributed setups where verification
      and signing happen in different services.

    """

    __slots__ = [
        "secret_key",
        "algorithm",
        "access_token_expire_minutes",
        "refresh_token_expire_days",
        "access_token_expire",
        "refresh_token_expire",
        "cookie_name",
        "cookie_secure",
        "cookie_httponly",
        "cookie_samesite",
    ]

    def __init__(
        self,
        secret_key: str,
        algorithm: Literal["HS256", "RS256"] = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7,
        cookie_name: str = "refresh_token",
        cookie_secure: bool = True,
        cookie_httponly: bool = True,
        cookie_samesite: Literal["strict", "lax", "none"] = "strict",
    ):
        """_summary
        Args:
            `secret_key` (Annotated[str, Doc): _description_
            `algorithm` (Literal[&quot;HS256&quot;, &quot;RS256&quot;], optional): _description_. Defaults to "HS256".
            `access_token_expire_minutes` (int, optional): _description_. Defaults to 15.
            `refresh_token_expire_days` (int, optional): _description_. Defaults to 7.
            `cookie_name` (str, optional): _description_. Defaults to "refresh_token".
            `cookie_secure` (bool, optional): _description_. Defaults to True.
            `cookie_httponly` (bool, optional): _description_. Defaults to True.
            `cookie_samesite` (Literal[&quot;strict&quot;, &quot;lax&quot;, &quot;none&quot;], optional): _description_. Defaults to "strict".
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)
        self.cookie_name = cookie_name
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.cookie_samesite = cookie_samesite

    def to_dict(self):
        """Convert config to dictionary representation."""
        return {
            "secret_key": "***REDACTED***",
            "algorithm": self.algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "refresh_token_expire_days": self.refresh_token_expire_days,
            "access_token_expire": str(self.access_token_expire),
            "refresh_token_expire": str(self.refresh_token_expire),
            "cookie_name": self.cookie_name,
            "cookie_secure": self.cookie_secure,
            "cookie_httponly": self.cookie_httponly,
            "cookie_samesite": self.cookie_samesite,
        }
