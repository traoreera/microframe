import json
import re
from datetime import datetime
from typing import Any


def filter_truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + suffix


def filter_slugify(text: str) -> str:
    return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", text.lower().strip()))


def filter_currency(value: float, symbol: str = "$", decimals: int = 2) -> str:
    return f"{symbol}{value:,.{decimals}f}"


def filter_timeago(dt: datetime) -> str:
    seconds = (datetime.now() - dt).total_seconds()
    for limit, label, divisor in (
        (60, None, None),
        (3600, "minute", 60),
        (86400, "heure", 3600),
        (None, "jour", 86400),
    ):
        if limit is None or seconds < limit:
            if divisor is None:
                return "à l'instant"
            value = int(seconds // divisor)
            return f"il y a {value} {label}{'s' if value > 1 else ''}"


def filter_json_pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False)
