from datetime import timedelta
from typing import  Optional
from dataclasses import dataclass, field
from starlette.responses import  Response
from starlette.requests import Request


@dataclass
class CookieConfig:
    expires: Optional[timedelta] 
    max_age: Optional[int] 
    domain: Optional[str]
    path: str = "/"
    secure: bool = False
    httponly: bool = False


class CookieResponse:

    def __init__(self, config:CookieConfig) -> None:
        self.config: CookieConfig = config
        return
    
    def set_cookie(
        self,
        response: Response,
        name: str,
        value: str,
    ) -> Response:
        
        response.set_cookie(
            key=name,
            value=value,
            expires= self.config.expires,
            max_age= self.config.max_age,
            path= self.config.path,
            domain= self.config.domain,
            secure= self.config.secure,
            httponly= self.config.httponly,
        )
        return response
    
    def delete_cookie(
        self,
        response: Response,
        name: str,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
    ) -> Response:
        response.delete_cookie(key=name, path=path, domain=domain, secure=secure, httponly=httponly)
        return response


    def update_cookies(self,response:Response,  name: str, value: str) -> Response:

        response.set_cookie(key=name, value=value)
        return response
    
    def cookies_response(self, request: Request) -> dict:
        return request.cookies



def get_cookie_response() -> CookieResponse:
    """Factory compatible Microframe/Starlette/FastAPI Depends()."""
    conf = CookieConfig(
        expires=timedelta(days=365),
        max_age= 365 * 24 * 60 * 60,
        domain="microframe.dev",
        path="/",
        secure=False,
        httponly=False
    )

    return CookieResponse(conf)
