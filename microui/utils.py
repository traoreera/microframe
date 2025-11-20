"""
Utility helpers for HTML generation
Reduces code duplication across microui components
"""
from typing import List, Dict, Optional
from markupsafe import Markup


def build_class_list(base_classes: List[str], additional: str = "") -> str:
    """Build a space-separated class string from a list and additional classes"""
    all_classes = base_classes + ([additional] if additional else [])
    return " ".join(filter(None, all_classes))


def build_hx_attrs(
    hx_get: Optional[str] = None,
    hx_post: Optional[str] = None,
    hx_put: Optional[str] = None,
    hx_delete: Optional[str] = None,
    hx_target: Optional[str] = None,
    hx_swap: Optional[str] = None,
    hx_trigger: Optional[str] = None,
    hx_vals: Optional[str] = None,
) -> str:
    """Build HTMX attributes string"""
    attrs = []
    if hx_get:
        attrs.append(f'hx-get="{hx_get}"')
    if hx_post:
        attrs.append(f'hx-post="{hx_post}"')
    if hx_put:
        attrs.append(f'hx-put="{hx_put}"')
    if hx_delete:
        attrs.append(f'hx-delete="{hx_delete}"')
    if hx_target:
        attrs.append(f'hx-target="{hx_target}"')
    if hx_swap:
        attrs.append(f'hx-swap="{hx_swap}"')
    if hx_trigger:
        attrs.append(f'hx-trigger="{hx_trigger}"')
    if hx_vals:
        attrs.append(f"hx-vals='{hx_vals}'")
    
    return " ".join(attrs)


def build_link(
    href: str,
    text: str,
    classes: str = "",
    hx_get: Optional[str] = None,
    hx_target: Optional[str] = None,
    hx_swap: Optional[str] = None,
) -> str:
    """Build an anchor tag with optional HTMX attributes"""
    hx_attrs = build_hx_attrs(hx_get=hx_get, hx_target=hx_target, hx_swap=hx_swap)
    class_attr = f'class="{classes}"' if classes else ""
    return f'<a href="{href}" {class_attr} {hx_attrs}>{text}</a>'

# Fonction utilitaire pour les items de menu avec support sous-menus
def build_menu_items(items: List[Dict], compact: bool = False) -> str:
    """Génère les items de menu avec sous-menus et tooltips pour mode compact"""
    html = ""
    for item in items:
        icon = item.get("icon", "")
        label = item.get("label", "")
        url = item.get("url", "#")
        active = item.get("active", False)
        badge = item.get("badge", "")
        submenu = item.get("submenu", [])
        
        active_class = "active" if active else ""
        badge_html = f'<span class="badge badge-sm">{badge}</span>' if badge else ""
        
        # Si il y a un sous-menu
        if submenu:
            submenu_items = ""
            for sub in submenu:
                sub_icon = sub.get("icon", "")
                sub_label = sub.get("label", "")
                sub_url = sub.get("url", "#")
                sub_active = sub.get("active", False)
                sub_active_class = "active" if sub_active else ""
                
                submenu_items += f"""
                <li><a href="{sub_url}" class="{sub_active_class}">{sub_icon} <span class="sidebar-label">{sub_label}</span></a></li>
                """
            
            html += f"""
            <li>
                <details>
                    <summary class="{active_class}">
                        {icon}
                        <span class="sidebar-label">{label}</span>
                        {badge_html}
                    </summary>
                    <ul>
                        {submenu_items}
                    </ul>
                </details>
            </li>
            """
        else:
            # Item simple sans sous-menu
            html += f"""
            <li>
                <a href="{url}" class="{active_class}">
                    {icon}
                    <span class="sidebar-label">{label}</span>
                    {badge_html}
                </a>
            </li>
            """
    
    return html


def build_feature_list(features: List[str], icon: str = "✓", icon_class: str = "text-success") -> str:
    """Build a feature list with checkmarks"""
    return "\n".join([
        f'<li class="flex items-center gap-2">'
        f'<span class="{icon_class}">{icon}</span> {feature}'
        f'</li>'
        for feature in features
    ])


# Common SVG icons cache
SVG_ICONS = {
    "chevron-down": '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-4 h-4 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>',
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>',
}


def get_svg_icon(name: str) -> str:
    """Get a cached SVG icon by name"""
    return SVG_ICONS.get(name, "")
