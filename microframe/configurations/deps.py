from typing import TypedDict

from .base import BaseCfg, Configure


class Logger(TypedDict):
    console: bool
    file: str
