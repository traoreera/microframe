from typing import Optional, Type

from .component import Component


class ComponentRegistry:
    """Registry for microui UI components.

    Components are registered by class and instantiated per render.
    Accessed by name (lowercased class name) at render time.
    """

    _components: dict = {}

    @classmethod
    def register(cls, name: str, component: Type[Component]):
        """Register a component class.

        Args:
            name: Component name (lowercase).
            component: Component class.
        """
        cls._components[name] = component

    @classmethod
    def get(cls, name: str) -> Optional[Type[Component]]:
        """Get a component class by name.

        Returns:
            The component class, or None if not found.
        """
        return cls._components.get(name)

    @classmethod
    def all(cls) -> dict:
        """Return all registered components."""
        return dict(cls._components)

    @classmethod
    def clear(cls):
        """Unregister all components."""
        cls._components.clear()


def register(cls):
    """Decorator that registers a Component subclass.

    Register a component class.

    Args:
        cls: A Component subclass with a ``render()`` method.

    Returns:
        The original class (unchanged).
    """
    if not hasattr(cls, "render"):
        raise TypeError(f"Component {cls.__name__} must have a render method.")
    ComponentRegistry.register(cls.__name__.lower(), cls)
    return cls
