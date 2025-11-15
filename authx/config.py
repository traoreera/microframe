"""
Configuration for the authentication system
"""

from datetime import timedelta
from typing import Annotated, Literal

from annotated_doc import Doc


class AuthConfig:
    """Configuration for the authentication system
    utilisation rapide:

    ```python
    from authx.config import AuthConfig
    auth = AuthConfig(secret_key="votre-cle-secrete-super-longue-et-complexe")
    ```
    - secret_key (str): secret key for the tokens
    - algorithm (str): cryptographic algorithm for the tokens (default HS256)
    - access_token_expire_minutes (int): lifetime of the access tokens (default 15 minutes)
    - refresh_token_expire_days (int): lifetime of the refresh tokens (default 7 days)
    - cookie_name (str): name of the cookie for storing the refresh token (default refresh_token)

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
        secret_key: Annotated[str, Doc("secret key for tokens")],
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

    def __dict__(self):
        return {
            "secret_key": self.__hash__(),
            "algorithm": self.algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "refresh_token_expire_days": self.refresh_token_expire_days,
            "access_token_expire": self.access_token_expire,
            "refresh_token_expire": self.refresh_token_expire,
            "cookie_name": self.cookie_name,
            "cookie_secure": self.cookie_secure,
            "cookie_httponly": self.cookie_httponly,
            "cookie_samesite": self.cookie_samesite,
        }


auth = AuthConfig(
    secret_key="votre-cle-secrete-super-longue-et-complexe",
)
