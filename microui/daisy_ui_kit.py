"""
Kit UI DaisyUI pour Python/HTMX
Composants réutilisables avec gestion des thèmes
"""

from typing import List, Literal, Optional

from markupsafe import Markup

# Importer les composants avancés
from .advance import (
    Avatar,
    Breadcrumb,
    Collapse,
    Divider,
    Drawer,
    Dropdown,
    Pagination,
    Progress,
    Sidebar,
    Skeleton,
    Stats,
    Swap,
    Tabs,
    Timeline,
    Toast,
    Tooltip,
)


class DaisyUI:
    """Gestionnaire de thèmes et composants DaisyUI"""

    THEMES = [
        "light",
        "dark",
        "cupcake",
        "bumblebee",
        "emerald",
        "corporate",
        "synthwave",
        "retro",
        "cyberpunk",
        "valentine",
        "halloween",
        "garden",
        "forest",
        "aqua",
        "lofi",
        "pastel",
        "fantasy",
        "wireframe",
        "black",
        "luxury",
        "dracula",
        "cmyk",
        "autumn",
        "business",
        "acid",
        "lemonade",
        "night",
        "coffee",
        "winter",
        "dim",
        "nord",
        "sunset",
    ]

    @staticmethod
    def theme_switcher(current_theme: str = "light", position: str = "dropdown-end") -> Markup:
        """Sélecteur de thème DaisyUI"""
        # Build theme items more efficiently
        theme_items = []
        for theme in DaisyUI.THEMES:
            icon = "🌙" if theme == "dark" else "☀️" if theme == "light" else "🎨"
            theme_items.append(
                f'<li>'
                f'<button class="theme-controller" '
                f'hx-post="/theme/set" '
                f'hx-vals=\'{{"theme": "{theme}"}}\' '
                f'hx-swap="outerHTML" '
                f'hx-target="body">'
                f'<span class="flex items-center gap-2">'
                f'{icon} {theme.capitalize()}'
                f'</span>'
                f'</button>'
                f'</li>'
            )
        
        themes_html = "\n".join(theme_items)

        # Icon selon le thème actuel
        current_icon = (
            "🌙" if current_theme == "dark" else "☀️" if current_theme == "light" else "🎨"
        )

        return Markup(
            f"""
        <div class="dropdown {position}">
            <div tabindex="0" role="button" class="btn btn-ghost gap-2">
                <span class="text-xl">{current_icon}</span>
                <span class="hidden sm:inline">{current_theme.capitalize()}</span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-4 h-4 stroke-current">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
            </div>
            <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow-2xl bg-base-300 rounded-box w-52 max-h-96 overflow-y-auto mt-4">
                {themes_html}
            </ul>
        </div>
        """
        )


class Button:
    """Composant Button DaisyUI"""

    @staticmethod
    def render(
        text: str,
        variant: Literal[
            "primary",
            "secondary",
            "accent",
            "ghost",
            "link",
            "info",
            "success",
            "warning",
            "error",
            "neutral",
            "outline",
        ] = "primary",
        size: Literal["xs", "sm", "md", "lg"] = "md",
        outline: bool = False,
        wide: bool = False,
        block: bool = False,
        loading: bool = False,
        disabled: bool = False,
        hx_get: Optional[str] = None,
        hx_post: Optional[str] = None,
        hx_target: Optional[str] = None,
        hx_swap: Optional[str] = None,
        onclick: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        css_classes = ["btn", f"btn-{variant}", f"btn-{size}"]

        if outline:
            css_classes.append(f"btn-outline")
        if wide:
            css_classes.append("btn-wide")
        if block:
            css_classes.append("btn-block")
        if loading:
            css_classes.append("loading")

        attrs = []
        if hx_get:
            attrs.append(f'hx-get="{hx_get}"')
        if hx_post:
            attrs.append(f'hx-post="{hx_post}"')
        if hx_target:
            attrs.append(f'hx-target="{hx_target}"')
        if hx_swap:
            attrs.append(f'hx-swap="{hx_swap}"')
        if onclick:
            attrs.append(f'onclick="{onclick}"')
        if disabled:
            attrs.append("disabled")

        all_classes = " ".join(css_classes + [classes])
        all_attrs = " ".join(attrs)

        return Markup(f'<button class="{all_classes}" {all_attrs}>{text}</button>')


class Card:
    """Composant Card DaisyUI"""

    @staticmethod
    def render(
        title: Optional[str] = None,
        body: str = "",
        image: Optional[str] = None,
        actions: Optional[str] = None,
        compact: bool = False,
        bordered: bool = False,
        side: bool = False,
        classes: str = "",
    ) -> Markup:
        css_classes = ["card", "bg-base-100"]

        if compact:
            css_classes.append("card-compact")
        if bordered:
            css_classes.append("border")
        if side:
            css_classes.append("card-side")

        image_html = (
            f'<figure><img src="{image}" alt="{title or "Card image"}" /></figure>' if image else ""
        )
        title_html = f"<h2 class='card-title'>{title}</h2>" if title else ""
        actions_html = f"<div class='card-actions justify-end'>{actions}</div>" if actions else ""

        return Markup(
            f"""
        <div class="card {' '.join(css_classes)} {classes}">
            {image_html}
            <div class="card-body">
                {title_html}
                {body}
                {actions_html}
            </div>
        </div>
        """
        )


class Alert:
    """Composant Alert DaisyUI"""

    @staticmethod
    def render(
        message: str,
        type: Literal["info", "success", "warning", "error"] = "info",
        dismissible: bool = False,
        icon: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        icons = {
            "info": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>',
            "success": '<svg xmlns="http://www.w3.org/2000/svg" class="stroke-success shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
            "warning": '<svg xmlns="http://www.w3.org/2000/svg" class="stroke-warning shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>',
            "error": '<svg xmlns="http://www.w3.org/2000/svg" class="stroke-error shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
        }

        icon_html = icon or icons.get(type, "")
        dismiss_html = (
            '<button class="btn btn-sm btn-circle btn-ghost" onclick="this.parentElement.remove()">✕</button>'
            if dismissible
            else ""
        )

        return Markup(
            f"""
        <div role="alert" class="alert alert-{type} {classes}">
            {icon_html}
            <span>{message}</span>
            {dismiss_html}
        </div>
        """
        )


class Modal:
    """Composant Modal DaisyUI"""

    @staticmethod
    def render(
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


class Input:
    """Composant Input DaisyUI"""

    @staticmethod
    def render(
        name: str,
        type: str = "text",
        placeholder: str = "",
        value: str = "",
        label: Optional[str] = None,
        size: Literal["xs", "sm", "md", "lg"] = "md",
        bordered: bool = True,
        error: Optional[str] = None,
        hx_post: Optional[str] = None,
        hx_trigger: Optional[str] = None,
        hx_target: Optional[str] = None,
        required: bool = True,
        classes: str = "",
    ) -> Markup:
        css_classes = ["input", f"input-{size}", "w-full"]
        if bordered:
            css_classes.append("input-bordered")
        if error:
            css_classes.append("input-error")

        attrs = []
        if hx_post:
            attrs.append(f'hx-post="{hx_post}"')
        if hx_trigger:
            attrs.append(f'hx-trigger="{hx_trigger}"')
        if hx_target:
            attrs.append(f'hx-target="{hx_target}"')

        label_html = (
            f'<label class="label"><span class="label-text">{label}</span></label>' if label else ""
        )
        error_html = (
            f'<label class="label"><span class="label-text-alt text-error">{error}</span></label>'
            if error
            else ""
        )
        all_attrs = " ".join(attrs)

        return Markup(
            f"""
        <div class="form-control {classes}">
            {label_html}
            <input type="{type}" name="{name}" placeholder="{placeholder}" value="{value}"  {"required" if required else "required"} class="{' '.join(css_classes)}" {all_attrs} />
            {error_html}
        </div>
        """
        )


class Table:
    """Composant Table DaisyUI"""

    @staticmethod
    def render(
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


class Badge:
    """Composant Badge DaisyUI"""

    @staticmethod
    def render(
        text: str,
        variant: Literal[
            "primary",
            "secondary",
            "accent",
            "ghost",
            "info",
            "success",
            "warning",
            "error",
            "neutral",
        ] = "neutral",
        size: Literal["xs", "sm", "md", "lg"] = "md",
        outline: bool = False,
        classes: str = "",
    ) -> Markup:
        css_classes = ["badge", f"badge-{variant}", f"badge-{size}"]
        if outline:
            css_classes.append("badge-outline")

        return Markup(f'<div class="{" ".join(css_classes)} {classes}">{text}</div>')


class Navbar:
    """Composant Navbar DaisyUI"""

    @staticmethod
    def render(
        brand: str, items: List[dict], end_items: Optional[str] = None, classes: str = ""
    ) -> Markup:
        nav_items = "".join(
            [
                f'<li><a href="{item.get("href", "#")}" '
                f'{"hx-get=\"" + item["hx_get"] + "\"" if item.get("hx_get") else ""}>'
                f'{item["text"]}</a></li>'
                for item in items
            ]
        )

        end_html = f'<div class="navbar-end">{end_items}</div>' if end_items else ""

        return Markup(
            f"""
        <div class="navbar bg-base-100 {classes}">
            <div class="navbar-start">
                <div class="dropdown">
                    <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
                        </svg>
                    </div>
                    <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                        {nav_items}
                    </ul>
                </div>
                <a class="btn btn-ghost text-xl">{brand}</a>
            </div>
            <div class="navbar-center hidden lg:flex">
                <ul class="menu menu-horizontal px-1">
                    {nav_items}
                </ul>
            </div>
            {end_html}
        </div>
        """
        )


class Loading:
    """Composant Loading DaisyUI"""

    @staticmethod
    def render(
        type: Literal["spinner", "dots", "ring", "ball", "bars", "infinity"] = "spinner",
        size: Literal["xs", "sm", "md", "lg"] = "md",
        color: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        css_classes = ["loading", f"loading-{type}", f"loading-{size}"]
        if color:
            css_classes.append(f"text-{color}")

        return Markup(f'<span class="{" ".join(css_classes)} {classes}"></span>')


# Helper pour enregistrer les composants
def register_components():
    """Enregistre tous les composants DaisyUI dans le registre"""
    # Basic
    return {
        "button": Button.render,
        "card": Card.render,
        "alert": Alert.render,
        "modal": Modal.render,
        "input": Input.render,
        "table": Table.render,
        "badge": Badge.render,
        "navbar": Navbar.render,
        "loading": Loading.render,
        "theme_switcher": DaisyUI.theme_switcher,
        # Advanced
        "sidebar": Sidebar.render,
        "drawer": Drawer.render,
        "breadcrumb": Breadcrumb.render,
        "tabs": Tabs.render,
        "dropdown": Dropdown.render,
        "avatar": Avatar.render,
        "progress": Progress.render,
        "stats": Stats.render,
        "timeline": Timeline.render,
        "collapse": Collapse.render,
        "divider": Divider.render,
        "toast": Toast.render,
        "pagination": Pagination.render,
        "skeleton": Skeleton.render,
        "tooltip": Tooltip.render,
        "swap": Swap.render,
    }
