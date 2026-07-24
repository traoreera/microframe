"""
MicroFrame — Moteur de rendu Jinja2

Usage:
    from microframe import TemplateEngine

    engine = TemplateEngine(directory="templates")
    html = await engine.render("index.html", {"title": "Accueil"})
"""

from microframe.engine.cache import CacheBackend, CacheManager
from microframe.engine.components import (ComponentRegistry,
                                          auto_register_components)
from microframe.engine.core import TemplateEngine
from microframe.engine.mfe import MFEClient
from microframe.engine.ui import Component as UIComponent
from microframe.engine.ui import register as ui_register
from microframe.engine.ui import render_microui

__all__ = [
    "TemplateEngine",
    "MFEClient",
    "CacheManager",
    "CacheBackend",
    "ComponentRegistry",
    "auto_register_components",
    "UIComponent",
    "ui_register",
    "render_microui",
]
