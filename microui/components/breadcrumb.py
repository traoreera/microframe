from typing import Dict, List

from markupsafe import Markup

from microui.core.extension import Component
from microui.core.register import register


@register
class Breadcrumb(Component):
    """Composant Breadcrumb pour navigation"""

    def render(self):
        return self.__render(items=self.props.get("items", []), classes=self.props.get("class", ""))

    @staticmethod
    def __render(items: List[Dict], classes: str = "") -> Markup:
        breadcrumb_items = []
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            if is_last:
                breadcrumb_items.append(f'<li>{item.get("text", "")}</li>')
            else:
                breadcrumb_items.append(
                    f'<li><a href="{item.get("href", "#")}">{item.get("text", "")}</a></li>'
                )

        return Markup(
            f"""
        <div class="text-sm breadcrumbs {classes}">
            <ul>
                {''.join(breadcrumb_items)}
            </ul>
        </div>
        """
        )
