from pathlib import Path


class ComponentRegistry:
    """Global registry for HTML components.

    Components are Jinja2 template strings (or file contents) registered
    by name. They can be used in templates via ``{% component "name" %}``
    or ``<component.name>`` syntax.

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
