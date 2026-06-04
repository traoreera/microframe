from pathlib import Path


class ComponentRegistry:
    _components: dict = {}

    @classmethod
    def register(cls, name: str, template: str):
        cls._components[name] = template

    @classmethod
    def get(cls, name: str):
        return cls._components.get(name)

    @classmethod
    def all(cls) -> dict:
        return dict(cls._components)


def auto_register_components(folder: str):
    """Auto-register all .html files in a folder as components."""
    path = Path(folder)
    if not path.exists():
        return
    for file in path.glob("*.html"):
        ComponentRegistry.register(file.stem, file.read_text())
