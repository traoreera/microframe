from pathlib import Path


class ComponentRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, template):
        cls._registry[name] = template

    @classmethod
    def get(cls, name: str):
        return cls._registry.get(name)


def auto_register_components(folder="templates/components"):
    folder = Path(folder)
    for file in folder.glob("*.html"):
        ComponentRegistry.register(file.stem, file.read_text())
        print(f"Registered component: {file.stem}")
