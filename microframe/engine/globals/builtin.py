import secrets
from typing import List


def generate_csrf_token() -> str:
    """Generate a cryptographically strong CSRF token.

    Available in templates as ``{{ csrf_token() }}``.
    Used internally by the ``<action>`` tag to populate hidden form inputs.
    """
    return secrets.token_urlsafe(32)


def paginate(items: list, page: int = 1, per_page: int = 10) -> dict:
    """Paginate a list of items.

    Available in templates as ``{{ paginate(items, page, per_page) }}``.

    Returns a dict with keys:
    ``results``, ``page``, ``per_page``, ``total``, ``total_pages``,
    ``has_prev``, ``has_next``, ``prev_page``, ``next_page``.
    """
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    return {
        "results": items[start : start + per_page],
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
    """Generate breadcrumb trail from a URL path.

    Available in templates as ``{{ breadcrumbs(request.path) }}``.

    Returns a list of dicts with ``name`` and ``url`` keys.
    """
    parts = [p for p in path.split("/") if p]
    crumbs = [{"name": "Accueil", "url": "/"}]
    current = ""
    for part in parts:
        current += f"/{part}"
        crumbs.append({"name": part.replace("-", " ").title(), "url": current})
    return crumbs
