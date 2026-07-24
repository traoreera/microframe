from markupsafe import Markup


class Component:
    """Base class for Python-based UI components (microui).

    Subclass and implement ``render()``, then decorate with ``@ui_register``
    to make the component available in templates via ``render_microui()``.

    Usage:
        @ui_register
        class Alert(Component):
            def render(self):
                return f'<div class="alert">{self.props.get("text", "")}</div>'
    """

    def __init__(self):
        self.props = {}
        self.children = None

    def render(self) -> Markup:
        """Render the component to HTML.

        Must be overridden by subclasses. Access props via ``self.props``
        and children/slot content via ``self.children`` or ``self.props.get("slot", "")``.

        Returns:
            HTML string or Markup object.
        """
        raise NotImplementedError("Each component must implement render.")
