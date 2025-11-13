from typing import TypedDict

from .base import BaseCfg, Configure


class JwtConfigSchemas(TypedDict):

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class JwtConfig(BaseCfg):
    def __init__(self, conf: Configure):
        super().__init__(conf, "jwt")
        self.default_migration: JwtConfigSchemas = {
            "secret_key": "your_secret_key",
            "algorithm": "HS256",
            "access_token_expire_minutes": 30,
            "refresh_token_expire_days": 7,
        }

        if self.conf is not None:
            self.custom_config: JwtConfigSchemas = self.conf
        else:
            self.custom_config = self.default_migration

    def __getattribute__(self, __name):
        return super().__getattribute__(__name)
