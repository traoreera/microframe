from markupsafe import Markup

from .registry import ComponentRegistry


def render_microui(component_name: str, **kwargs) -> Markup:
    """Render a microui component by name.

    Available in templates as ``{{ render_microui("name", **props) }}``
    when ``TemplateEngine(..., enable_ui=True)``.

    Args:
        component_name: Registered component name (case-insensitive).
        **kwargs: Props forwarded to the component's ``render()`` method.

    Returns:
        Markup-safe HTML string, or a comment if the component is not found.
    """
    component_cls = ComponentRegistry.get(component_name.lower())
    if not component_cls:
        return Markup(f"<!-- microui '{component_name}' not found -->")

    instance = component_cls()
    instance.props = dict(kwargs)
    instance.children = kwargs.get("children")

    html = instance.render()
    return Markup(html)


def setup_microui(env):
    """Register ``render_microui`` as a Jinja2 global."""
    env.globals["render_microui"] = render_microui
