"""
Routes de démonstration du TemplateManager (Jinja2 + HTMX)
"""

from microframe.routing import Router
from microframe.dependencies.exceptionHandler import Depends
from microframe.templating import get_templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

router = Router(
    prefix="/demo",
    tags=["templates", "htmx"]
)


@router.get("/", summary="Page d'accueil")
async def index(
    request: Request,
    templates=Depends(get_templates)
) -> HTMLResponse:
    """
    Page principale — rend index.html
    """
    context = {"title": "Accueil", "message": "Bienvenue dans ton moteur de template HTMX-ready 🚀"}
    return await templates.render("index.html", context, request)


@router.get("/users", summary="Liste utilisateurs")
async def users(
    request: Request,
    templates=Depends(get_templates)
) -> HTMLResponse:
    """
    Page /demo/users — rend un tableau avec htmx
    """
    users_data = [
        {"id": 1, "name": "Alice", "role": "Admin"},
        {"id": 2, "name": "Bob", "role": "User"},
        {"id": 3, "name": "Charlie", "role": "Moderator"},
    ]
    context = {"users": users_data, "title": "Liste des utilisateurs"}
    return await templates.render("partials/users_list.html", context, request)


@router.get("/cards", summary="Composants dynamiques")
async def cards(
    request: Request,
    templates=Depends(get_templates)
) -> HTMLResponse:
    """
    Affiche plusieurs cartes (test components/card.html)
    """
    cards_data = [
        {"title": "Serveur", "content": "Uptime 99.9%"},
        {"title": "Base de données", "content": "PostgreSQL 16"},
        {"title": "Redis Cache", "content": "Actif"},
    ]
    context = {"cards": cards_data, "title": "Status Système"}
    return await templates.render("partials/cards_demo.html", context, request)


@router.get("/htmx-refresh", summary="Test HX-Refresh")
async def htmx_refresh(
    request: Request,
    templates=Depends(get_templates)
):
    """
    Teste un rendu partiel avec HX-Refresh.
    """
    context = {"hx_refresh": True}
    return await templates.render("partials/htmx_loader.html", context, request)
