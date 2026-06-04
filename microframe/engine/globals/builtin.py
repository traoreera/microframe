import hashlib
import time
from typing import List


def generate_csrf_token() -> str:
    token = hashlib.sha256(f"{time.time()}".encode()).hexdigest()
    return f"<input type='hidden' name='csrf_token' value='{token}'>"


def paginate(items: list, page: int = 1, per_page: int = 10) -> dict:
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    return {
        "results": items[start: start + per_page],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": page < total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
    }


def breadcrumbs(path: str = "/") -> List[dict]:
    parts = [p for p in path.split("/") if p]
    crumbs = [{"name": "Accueil", "url": "/"}]
    current = ""
    for part in parts:
        current += f"/{part}"
        crumbs.append({"name": part.replace("-", " ").title(), "url": current})
    return crumbs
