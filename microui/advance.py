"""
Composants avancés DaisyUI : Sidebar, Drawer, Breadcrumb, Tabs, etc.
"""

from typing import Dict, List, Literal, Optional

from markupsafe import Markup


class Sidebar:
    """Composant Sidebar avec menu"""

    @staticmethod
    def render(
        items: List[Dict],
        brand: Optional[str] = None,
        brand_logo: Optional[str] = None,
        footer: Optional[str] = None,
        compact: bool = False,
        classes: str = "",
    ) -> Markup:
        brand_html = ""
        if brand or brand_logo:
            logo = f'<img src="{brand_logo}" class="w-8 h-8" />' if brand_logo else ""
            brand_html = f"""
            <li class="mb-2">
                <a class="flex items-center gap-2 font-bold text-lg">
                    {logo}
                    {brand or ""}
                </a>
            </li>
            """

        menu_items = ""
        for item in items:
            icon = item.get("icon", "")
            active = "active" if item.get("active", False) else ""
            submenu = item.get("submenu", [])

            if submenu:
                # Menu avec sous-menu
                submenu_items = "".join(
                    [
                        f'<li><a href="{sub.get("href", "#")}">{sub.get("text", "")}</a></li>'
                        for sub in submenu
                    ]
                )
                menu_items += f"""
                <li>
                    <details>
                        <summary>{icon} {item.get("text", "")}</summary>
                        <ul>{submenu_items}</ul>
                    </details>
                </li>
                """
            else:
                # Menu simple
                hx_attrs = ""
                if item.get("hx_get"):
                    hx_attrs = f'hx-get="{item["hx_get"]}" hx-target="{item.get("hx_target", "#content")}" hx-swap="{item.get("hx_swap", "innerHTML")}"'

                menu_items += f"""
                <li>
                    <a href="{item.get("href", "#")}" class="{active}" {hx_attrs}>
                        {icon} {item.get("text", "")}
                    </a>
                </li>
                """

        footer_html = f'<div class="p-4 border-t border-base-300">{footer}</div>' if footer else ""

        size_class = "w-64" if not compact else "w-20"

        return Markup(
            f"""
        <div class="drawer-side z-40">
            <label for="sidebar-drawer" class="drawer-overlay"></label>
            <aside class="menu {size_class} min-h-screen bg-base-200 text-base-content {classes}">
                <ul class="p-4">
                    {brand_html}
                    {menu_items}
                </ul>
                {footer_html}
            </aside>
        </div>
        """
        )


class Drawer:
    """Composant Drawer pour sidebar responsive"""

    @staticmethod
    def render(
        sidebar_content: str,
        main_content: str,
        drawer_id: str = "sidebar-drawer",
        classes: str = "",
    ) -> Markup:
        return Markup(
            f"""
        <div class="drawer lg:drawer-open {classes}">
            <input id="{drawer_id}" type="checkbox" class="drawer-toggle" />
            
            <div class="drawer-content flex flex-col">
                {main_content}
            </div>
            
            {sidebar_content}
        </div>
        """
        )


class Breadcrumb:
    """Composant Breadcrumb pour navigation"""

    @staticmethod
    def render(items: List[Dict], classes: str = "") -> Markup:
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


class Tabs:
    """Composant Tabs"""

    @staticmethod
    def render(
        tabs: List[Dict],
        variant: Literal["bordered", "lifted", "boxed"] = "bordered",
        size: Literal["xs", "sm", "md", "lg"] = "md",
        classes: str = "",
    ) -> Markup:
        tabs_html = []
        content_html = []

        for i, tab in enumerate(tabs):
            tab_id = tab.get("id", f"tab_{i}")
            active = "tab-active" if tab.get("active", False) else ""

            tabs_html.append(
                f"""
            <a class="tab tab-{size} {active}" 
               onclick="document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden')); 
                        document.getElementById('{tab_id}_content').classList.remove('hidden');
                        document.querySelectorAll('.tab').forEach(t => t.classList.remove('tab-active'));
                        this.classList.add('tab-active');">
                {tab.get("text", "")}
            </a>
            """
            )

            content_display = "" if tab.get("active", False) else "hidden"
            content_html.append(
                f"""
            <div id="{tab_id}_content" class="tab-content {content_display} p-4">
                {tab.get("content", "")}
            </div>
            """
            )

        return Markup(
            f"""
        <div class="{classes}">
            <div role="tablist" class="tabs tabs-{variant}">
                {''.join(tabs_html)}
            </div>
            <div class="tab-container">
                {''.join(content_html)}
            </div>
        </div>
        """
        )


class Dropdown:
    """Composant Dropdown"""

    @staticmethod
    def render(
        button_text: str,
        items: List[Dict],
        position: Literal[
            "dropdown-end", "dropdown-top", "dropdown-bottom", "dropdown-left", "dropdown-right"
        ] = "dropdown-end",
        classes: str = "",
    ) -> Markup:
        menu_items = []
        for item in items:
            if item.get("divider"):
                menu_items.append('<li><hr class="my-2" /></li>')
            else:
                menu_items.append(
                    f"""
                <li>
                    <a href="{item.get("href", "#")}" 
                       {'hx-get="' + item["hx_get"] + '"' if item.get("hx_get") else ''}>
                        {item.get("icon", "")} {item.get("text", "")}
                    </a>
                </li>
                """
                )

        return Markup(
            f"""
        <div class="dropdown {position} {classes}">
            <div tabindex="0" role="button" class="btn m-1">{button_text}</div>
            <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                {''.join(menu_items)}
            </ul>
        </div>
        """
        )


class Avatar:
    """Composant Avatar"""

    @staticmethod
    def render(
        src: str,
        alt: str = "Avatar",
        size: Literal["xs", "sm", "md", "lg", "xl"] = "md",
        shape: Literal["circle", "square"] = "circle",
        online: bool = False,
        offline: bool = False,
        placeholder: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        size_map = {"xs": "w-8", "sm": "w-12", "md": "w-16", "lg": "w-24", "xl": "w-32"}
        size_class = size_map.get(size, "w-16")

        shape_class = "rounded-full" if shape == "circle" else "rounded-xl"

        status = ""
        if online:
            status = "online"
        elif offline:
            status = "offline"

        if placeholder:
            return Markup(
                f"""
            <div class="avatar placeholder {status} {classes}">
                <div class="bg-neutral text-neutral-content {shape_class} {size_class}">
                    <span>{placeholder}</span>
                </div>
            </div>
            """
            )

        return Markup(
            f"""
        <div class="avatar {status} {classes}">
            <div class="{shape_class} {size_class}">
                <img src="{src}" alt="{alt}" />
            </div>
        </div>
        """
        )


class Progress:
    """Composant Progress Bar"""

    @staticmethod
    def render(
        value: int,
        max: int = 100,
        color: Optional[str] = None,
        size: Literal["xs", "sm", "md", "lg"] = "md",
        classes: str = "",
    ) -> Markup:
        color_class = f"progress-{color}" if color else ""
        size_class = f"progress-{size}" if size != "md" else ""

        return Markup(
            f"""
        <progress class="progress {color_class} {size_class} {classes}" 
                  value="{value}" max="{max}"></progress>
        """
        )


class Stats:
    """Composant Stats"""

    @staticmethod
    def render(stats: List[Dict], vertical: bool = False, classes: str = "") -> Markup:
        orientation = "stats-vertical" if vertical else "stats-horizontal"

        stats_html = []
        for stat in stats:
            icon = (
                f'<div class="stat-figure text-{stat.get("color", "primary")}">{stat.get("icon", "")}</div>'
                if stat.get("icon")
                else ""
            )

            stats_html.append(
                f"""
            <div class="stat">
                {icon}
                <div class="stat-title">{stat.get("title", "")}</div>
                <div class="stat-value text-{stat.get("color", "primary")}">{stat.get("value", "")}</div>
                <div class="stat-desc">{stat.get("desc", "")}</div>
            </div>
            """
            )

        return Markup(
            f"""
        <div class="stats shadow {orientation} {classes}">
            {''.join(stats_html)}
        </div>
        """
        )


class Timeline:
    """Composant Timeline"""

    @staticmethod
    def render(
        items: List[Dict],
        compact: bool = False,
        snap: bool = False,
        vertical: bool = True,
        classes: str = "",
    ) -> Markup:
        timeline_classes = ["timeline"]
        if compact:
            timeline_classes.append("timeline-compact")
        if snap:
            timeline_classes.append("timeline-snap-icon")
        if vertical:
            timeline_classes.append("timeline-vertical")
        else:
            timeline_classes.append("timeline-horizontal")

        items_html = []
        for i, item in enumerate(items):
            icon = item.get("icon", f'<div class="text-xl">{i+1}</div>')
            position = "timeline-start" if i % 2 == 0 else "timeline-end"

            items_html.append(
                f"""
            <li>
                <div class="timeline-middle">{icon}</div>
                <div class="{position} timeline-box">
                    {item.get("title") and f'<div class="font-bold">{item["title"]}</div>' or ''}
                    {item.get("content", "")}
                    {item.get("date") and f'<div class="text-xs text-gray-500 mt-2">{item["date"]}</div>' or ''}
                </div>
                <hr />
            </li>
            """
            )

        return Markup(
            f"""
        <ul class="{' '.join(timeline_classes)} {classes}">
            {''.join(items_html)}
        </ul>
        """
        )


class Collapse:
    """Composant Collapse (Accordion)"""

    @staticmethod
    def render(
        items: List[Dict], arrow: bool = True, plus: bool = False, classes: str = ""
    ) -> Markup:
        icon_class = "collapse-arrow" if arrow else ("collapse-plus" if plus else "collapse-close")

        collapses = []
        for i, item in enumerate(items):
            open_attr = "checked" if item.get("open", False) else ""

            collapses.append(
                f"""
            <div class="collapse {icon_class} bg-base-200 mb-2">
                <input type="radio" name="collapse-{id(items)}" {open_attr} />
                <div class="collapse-title text-xl font-medium">
                    {item.get("title", "")}
                </div>
                <div class="collapse-content">
                    {item.get("content", "")}
                </div>
            </div>
            """
            )

        return Markup(
            f"""
        <div class="{classes}">
            {''.join(collapses)}
        </div>
        """
        )


class Divider:
    """Composant Divider"""

    @staticmethod
    def render(
        text: Optional[str] = None,
        vertical: bool = False,
        color: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        orientation = "divider-vertical" if vertical else "divider-horizontal"
        color_class = f"divider-{color}" if color else ""

        return Markup(
            f"""
        <div class="divider {orientation} {color_class} {classes}">
            {text or ""}
        </div>
        """
        )


class Toast:
    """Composant Toast pour notifications"""

    @staticmethod
    def render(
        message: str,
        type: Literal["info", "success", "warning", "error"] = "info",
        position: Literal[
            "top-start",
            "top-center",
            "top-end",
            "middle-start",
            "middle-center",
            "middle-end",
            "bottom-start",
            "bottom-center",
            "bottom-end",
        ] = "top-end",
        classes: str = "",
    ) -> Markup:
        position_map = {
            "top-start": "toast-top toast-start",
            "top-center": "toast-top toast-center",
            "top-end": "toast-top toast-end",
            "middle-start": "toast-middle toast-start",
            "middle-center": "toast-middle toast-center",
            "middle-end": "toast-middle toast-end",
            "bottom-start": "toast-bottom toast-start",
            "bottom-center": "toast-bottom toast-center",
            "bottom-end": "toast-bottom toast-end",
        }

        return Markup(
            f"""
        <div class="toast {position_map.get(position, 'toast-top toast-end')} {classes}">
            <div class="alert alert-{type}">
                <span>{message}</span>
            </div>
        </div>
        """
        )


class Pagination:
    """Composant Pagination"""

    @staticmethod
    def render(
        current_page: int,
        total_pages: int,
        base_url: str,
        size: Literal["xs", "sm", "md", "lg"] = "md",
        classes: str = "",
    ) -> Markup:
        size_class = f"join-{size}" if size != "md" else ""

        pages_html = []

        # Bouton précédent
        prev_disabled = "btn-disabled" if current_page <= 1 else ""
        pages_html.append(
            f"""
        <a href="{base_url}?page={current_page - 1}" 
           class="join-item btn {prev_disabled}">«</a>
        """
        )

        # Pages
        start = max(1, current_page - 2)
        end = min(total_pages, current_page + 2)

        for page in range(start, end + 1):
            active = "btn-active" if page == current_page else ""
            pages_html.append(
                f"""
            <a href="{base_url}?page={page}" 
               class="join-item btn {active}">{page}</a>
            """
            )

        # Bouton suivant
        next_disabled = "btn-disabled" if current_page >= total_pages else ""
        pages_html.append(
            f"""
        <a href="{base_url}?page={current_page + 1}" 
           class="join-item btn {next_disabled}">»</a>
        """
        )

        return Markup(
            f"""
        <div class="join {size_class} {classes}">
            {''.join(pages_html)}
        </div>
        """
        )


class Skeleton:
    """Composant Skeleton pour loading states"""

    @staticmethod
    def render(
        type: Literal["text", "avatar", "card", "custom"] = "text",
        lines: int = 3,
        classes: str = "",
    ) -> Markup:
        if type == "avatar":
            return Markup(
                f"""
            <div class="flex items-center gap-4 {classes}">
                <div class="skeleton w-16 h-16 rounded-full shrink-0"></div>
                <div class="flex flex-col gap-4 flex-1">
                    <div class="skeleton h-4 w-full"></div>
                    <div class="skeleton h-4 w-3/4"></div>
                </div>
            </div>
            """
            )

        elif type == "card":
            return Markup(
                f"""
            <div class="flex flex-col gap-4 {classes}">
                <div class="skeleton h-32 w-full"></div>
                <div class="skeleton h-4 w-full"></div>
                <div class="skeleton h-4 w-3/4"></div>
            </div>
            """
            )

        else:  # text
            lines_html = "".join(
                [
                    f'<div class="skeleton h-4 w-{"full" if i == 0 else "3/4" if i == lines-1 else "full"}"></div>'
                    for i in range(lines)
                ]
            )
            return Markup(
                f"""
            <div class="flex flex-col gap-4 {classes}">
                {lines_html}
            </div>
            """
            )


class Tooltip:
    """Composant Tooltip"""

    @staticmethod
    def render(
        content: str,
        text: str,
        position: Literal["top", "bottom", "left", "right"] = "top",
        color: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        color_class = f"tooltip-{color}" if color else ""

        return Markup(
            f"""
        <div class="tooltip tooltip-{position} {color_class} {classes}" data-tip="{text}">
            {content}
        </div>
        """
        )


class Swap:
    """Composant Swap pour icônes toggle"""

    @staticmethod
    def render(
        on_icon: str, off_icon: str, rotate: bool = False, flip: bool = False, classes: str = ""
    ) -> Markup:
        effect = "swap-rotate" if rotate else ("swap-flip" if flip else "")

        return Markup(
            f"""
        <label class="swap {effect} {classes}">
            <input type="checkbox" />
            <div class="swap-on">{on_icon}</div>
            <div class="swap-off">{off_icon}</div>
        </label>
        """
        )
