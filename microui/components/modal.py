from typing import Optional

from markupsafe import Markup

from microui.core.extension import Component
from microui.core.register import register


@register
class Modal(Component):
    """Composant Modal DaisyUI"""

    def render(self):
        return self.__render(
            id=self.props.get("id", "my_modal"),
            title=self.props.get("title", ""),
            content=self.props.get("content", self.children or ""),
            actions=self.props.get("actions"),
            classes=self.props.get("class", ""),
        )

    @staticmethod
    def __render(
        id: str, title: str, content: str, actions: Optional[str] = None, classes: str = ""
    ) -> Markup:
        actions_html = actions or f'<button class="btn" onclick="{id}.close()">Fermer</button>'

        return Markup(
            f"""
        <dialog id="{id}" class="modal {classes}">
            <div class="modal-box">
                <h3 class="font-bold text-lg">{title}</h3>
                <div class="py-4">{content}</div>
                <div class="modal-action">
                    <form method="dialog">
                        {actions_html}
                    </form>
                </div>
            </div>
            <form method="dialog" class="modal-backdrop">
                <button>close</button>
            </form>
        </dialog>
        """
        )
