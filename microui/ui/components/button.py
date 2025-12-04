from markupsafe import Markup
from microui.core.extension import Component


class Button(Component):
    """Composant DaisyUI (Python)"""

    is_raw = True  # ← IMPORTANT : empêche Jinja de tenter de compiler

    def render(self):

        # --- BASE CSS ---
        css = ["btn"]

        # --- ATTRIBUTS HTML / HTMX QUI RESTENT ---
        html_attrs = {}

        for key, value in self.props.items():

            # --- Classes DaisyUI ---
            if key in ("variant", "size"):
                css.append(f"btn-{value}")
                continue

            if key in ("wide", "block"):
                css.append(f"btn-{key}")
                continue

            if key in ("loading", "disabled"):
                css.append(key)
                continue

            # --- Enfants internes (slot) ---
            if key == "children":
                continue

            # --- Tous les autres = htmx ou attribut normal ---
            html_attrs[f"hx-{key}"] = value

        # --- Slot content ---
        children = self.props.get("children", "")
        if not isinstance(children, str):
            children = str(children)

        # --- Génération attribs HTML safely ---
        attrs = " ".join(f'{k}="{v}"' for k, v in html_attrs.items())

        return Markup(
            f'<button class="{" ".join(css)}" {attrs}>{children}</button>'
        )
