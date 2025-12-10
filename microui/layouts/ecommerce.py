from typing import Optional

from markupsafe import Markup

from microui.components import Avatar, Drawer, Dropdown, Navbar, Sidebar, ThemeSwitcher
from microui.core.extension import Component
from microui.core.register import register


@register
class EcommerceLayout(Component):
    """An e-commerce layout with a shopping cart in the navbar."""

    def render(self):
        return self.__render(
            title=self.props.get("title", "E-commerce"),
            main_content=self.props.get("main_content", self.children or ""),
            cart_item_count=self.props.get("cart_item_count", 0),
            user_name=self.props.get("user_name", "Anonymous"),
            avatar_src=self.props.get("avatar_src"),
            brand_text=self.props.get("brand_text", "My Shop"),
            theme=self.props.get("theme", "light"),
            classes=self.props.get("class", ""),
        )

    @staticmethod
    def __render(
        title: str,
        main_content: str,
        cart_item_count: int = 0,
        user_name: str = "Anonymous",
        avatar_src: Optional[str] = None,
        brand_text: str = "My Shop",
        theme: str = "light",
        classes: str = "",
    ) -> Markup:

        user_menu_dropdown = Dropdown.rendering(
            button_text=f"""
                <div class="flex items-center gap-2">
                    {Avatar.rendering(src=avatar_src, placeholder=user_name[0] if user_name else 'A', size="xs", shape="circle")}
                    <span class="hidden md:inline">{user_name}</span>
                </div>
            """,
            items=[
                {"text": "My Orders", "href": "/orders", "icon": "📦"},
                {"text": "Profile", "href": "/profile", "icon": "👤"},
                {"text": "Settings", "href": "/settings", "icon": "⚙️"},
                {"divider": True},
                {"text": "Logout", "href": "/logout", "icon": "🚪"},
            ],
            position="dropdown-end",
        )

        shopping_cart_icon = Markup(
            f"""
            <div class="dropdown dropdown-end">
                <label tabindex="0" class="btn btn-ghost btn-circle">
                    <div class="indicator">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                        <span class="badge badge-sm indicator-item">{cart_item_count}</span>
                    </div>
                </label>
                <div tabindex="0" class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow">
                    <div class="card-body">
                        <span class="font-bold text-lg">{cart_item_count} Items</span>
                        <span class="text-info">Subtotal: $999</span>
                        <div class="card-actions">
                            <a href="/cart" class="btn btn-primary btn-block">View cart</a>
                        </div>
                    </div>
                </div>
            </div>
        """
        )

        navbar_content = Navbar.rendering(
            brand=brand_text,
            items=[
                {"text": "Home", "href": "/"},
                {"text": "Shop", "href": "/shop"},
                {"text": "About", "href": "/about"},
            ],
            end_items=f"""
                <div class="flex items-center gap-4">
                    {shopping_cart_icon}
                    {ThemeSwitcher.rendering(current_theme=theme)}
                    {user_menu_dropdown}
                </div>
            """,
        )

        return Markup(
            f"""
        <!DOCTYPE html>
        <html lang="en" data-theme="{theme}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} | {brand_text}</title>
            <link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css" rel="stylesheet" type="text/css" />
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@1.9.10" defer></script>
        </head>
        <body class="{classes}">
            {navbar_content}
            <main class="p-4 sm:p-6 lg:p-8">
                {main_content}
            </main>
        </body>
        </html>
        """
        )
