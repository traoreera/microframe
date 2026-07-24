import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ComponentRegistry:
    """Global registry for HTML components.

    Components are Jinja2 template strings (or file contents) registered
    by name. They can be used in templates via ``{% component "name" %}``
    or ``<component.name>`` syntax.

    This registry is process-global and flat, keyed only by name — it is
    NOT scoped per TemplateEngine instance or per template namespace (see
    `namespaces` in build_environment for template-level scoping). Two
    plugins registering a component under the same name will collide;
    `register()` logs a warning when that happens rather than overwriting
    silently. Prefix plugin-specific component filenames uniquely (e.g.
    `blog_card.html`, `crm_card.html`) to avoid the collision entirely.

    Usage:
        ComponentRegistry.register("alert", "<div class='alert'>{{ slot }}</div>")
        template = ComponentRegistry.get("alert")
    """

    _components: dict = {}

    @classmethod
    def register(cls, name: str, template: str):
        """Register a component by name.

        Args:
            name: Component name (lowercase, used in templates).
            template: Jinja2 template string for the component.
        """
        existing = cls._components.get(name)
        if existing is not None and existing != template:
            logger.warning(
                "Component '%s' re-registered with different content — "
                "the previous definition is now shadowed. Rename one of the "
                "source files to avoid this collision.",
                name,
            )
        cls._components[name] = template

    @classmethod
    def get(cls, name: str):
        """Get a component template by name.

        Returns:
            The template string, or None if not found.
        """
        return cls._components.get(name)

    @classmethod
    def all(cls) -> dict:
        """Return all registered components as a dict."""
        return dict(cls._components)


def auto_register_components(folder: str):
    """Auto-register all .html files in a folder as components.

    Scans the given folder for ``*.html`` files and registers each one
    using its filename (without extension) as the component name.

    Args:
        folder: Path to the components directory.
    """
    path = Path(folder)
    if not path.exists():
        return
    for file in path.glob("*.html"):
        ComponentRegistry.register(file.stem, file.read_text())
