"""
MicroFrame — Moteur de rendu Jinja2

Usage:
    from microframe import TemplateEngine

    engine = TemplateEngine(directory="templates")
    html = await engine.render("index.html", {"title": "Accueil"})
"""

from microframe.engine.cache import CacheBackend, CacheManager
from microframe.engine.components import ComponentRegistry, auto_register_components
from microframe.engine.core import TemplateEngine
from microframe.engine.mfe import MFEClient

__all__ = [
    "TemplateEngine",
    "MFEClient",
    "CacheManager",
    "CacheBackend",
    "ComponentRegistry",
    "auto_register_components",
]
