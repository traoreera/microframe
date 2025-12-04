from typing import Dict, Optional
from pathlib import Path
from starlette.requests import Request

from .component import ComponentRegistry
from .engine import TemplateEngine


def get_engine():
    """You can also use it with `Depends`"""
    return TemplateEngine.instance()


async def render(template_name: str, ctx: Optional[Dict] = None, request: Optional[Request] = None):
    return await get_engine().render(template_name, ctx, request)


def list_templates():
    return get_engine().env.list_templates()


def register_mfe(name: str, url: str):
    """Register a micro-frontend"""
    get_engine().register_mfe(name, url)


def register_mfes(mfes: Dict[str, str]):
    """Register multiple micro-frontends"""
    get_engine().register_mfes(mfes)

def auto_register_components(folder):
    """Auto-register components from folder.
    
    Args:
        folder (str): path to folder containing components
    """
    folder = Path(folder)
    if not folder.exists():
        raise NotADirectoryError(f"Folder not found: {folder}")
    
    for file in folder.glob("*.html"):
        try:
            ComponentRegistry.register(file.stem, file.read_text(encoding="utf-8"))
            count += 1
        except Exception as e:
            raise e from e


def register_component(name: str, template: str):
    """Register a single component."""
    ComponentRegistry.register(name, template)


def register_components(components: dict):
    """Register multiple components at once."""
    for name, template in components.items():
        ComponentRegistry.register(name, template)