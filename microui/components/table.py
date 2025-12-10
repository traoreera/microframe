from typing import List

from markupsafe import Markup

from microui.core.extension import Component
from microui.core.register import register


@register
class Table(Component):
    """Composant Table DaisyUI"""

    def render(self):
        return self.__render(
            headers=self.props.get("headers", []),
            rows=self.props.get("rows", []),
            zebra=self.props.get("zebra", False),
            compact=self.props.get("compact", False),
            hoverable=self.props.get("hoverable", True),
            classes=self.props.get("class", ""),
        )

    @staticmethod
    def __render(
        headers: List[str],
        rows: List[List[str]],
        zebra: bool = False,
        compact: bool = False,
        hoverable: bool = True,
        classes: str = "",
    ) -> Markup:
        css_classes = ["table"]
        if zebra:
            css_classes.append("table-zebra")
        if compact:
            css_classes.append("table-xs")

        headers_html = "".join([f"<th>{h}</th>" for h in headers])

        rows_html = ""
        for row in rows:
            row_class = "hover" if hoverable else ""
            cells_html = "".join([f"<td>{cell}</td>" for cell in row])
            rows_html += f"<tr class='{row_class}'>{cells_html}</tr>"

        return Markup(
            f"""
        <div class="overflow-x-auto">
            <table class="{' '.join(css_classes)} {classes}">
                <thead>
                    <tr>{headers_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """
        )
