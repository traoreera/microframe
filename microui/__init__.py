"""
MicroUI - DaisyUI components for Python/HTMX
Lazy loading for improved performance
"""
import typing

if typing.TYPE_CHECKING:
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
    from .daisy_ui_kit import (
        Alert,
        Badge,
        Button,
        Card,
        DaisyUI,
        Input,
        Loading,
        Modal,
        Navbar,
        Table,
        register_components,
    )
    from .thems import (
        ThemeManager,
        create_theme_routes,
        get_theme_context,
        register_theme_helpers,
        setup_daisy_ui,
    )
    from .layout import (
        Contact,
        Pricing,
    )
    from .layout_pages import (
        DashBordLayout,
        EcommerceLayout,
        LandingPage,
        KanbanLayout,
    )
    from .pages import (
        LoginConfig,
        RegisterConfig,
        ProfileConfig,
        UsersManagementConfig,
        SettingsConfig,
        AuthComponents,
        AuthPages,
        ProfilePages,
        UsersManagement,
        SettingsPages,
    )

__all__ = [
    # Basic components
    "DaisyUI",
    "Button",
    "Card",
    "Alert",
    "Modal",
    "Input",
    "Table",
    "Badge",
    "Navbar",
    "Loading",
    # Advanced components
    "Sidebar",
    "Drawer",
    "Breadcrumb",
    "Tabs",
    "Dropdown",
    "Avatar",
    "Progress",
    "Stats",
    "Timeline",
    "Collapse",
    "Divider",
    "Toast",
    "Pagination",
    "Skeleton",
    "Tooltip",
    "Swap",
    # Layout components
    "Pricing",
    "Contact",
    # Page layouts
    "DashBordLayout",
    "LandingPage",
    "KanbanLayout",
    "EcommerceLayout",
    # Pages module
    "LoginConfig",
    "RegisterConfig",
    "ProfileConfig",
    "UsersManagementConfig",
    "SettingsConfig",
    "AuthComponents",
    "AuthPages",
    "ProfilePages",
    "UsersManagement",
    "SettingsPages",
    # Helper functions and utils
    "register_components",
    "setup_daisy_ui",
    "ThemeManager",
    "get_theme_context",
    "register_theme_helpers",
    "create_theme_routes",
]

# Lazy import mapping
_import_map = {
    # Basic components from daisy_ui_kit
    "DaisyUI": ("microui.daisy_ui_kit", "DaisyUI"),
    "Button": ("microui.daisy_ui_kit", "Button"),
    "Card": ("microui.daisy_ui_kit", "Card"),
    "Alert": ("microui.daisy_ui_kit", "Alert"),
    "Modal": ("microui.daisy_ui_kit", "Modal"),
    "Input": ("microui.daisy_ui_kit", "Input"),
    "Table": ("microui.daisy_ui_kit", "Table"),
    "Badge": ("microui.daisy_ui_kit", "Badge"),
    "Navbar": ("microui.daisy_ui_kit", "Navbar"),
    "Loading": ("microui.daisy_ui_kit", "Loading"),
    "register_components": ("microui.daisy_ui_kit", "register_components"),
    # Advanced components from advance
    "Sidebar": ("microui.advance", "Sidebar"),
    "Drawer": ("microui.advance", "Drawer"),
    "Breadcrumb": ("microui.advance", "Breadcrumb"),
    "Tabs": ("microui.advance", "Tabs"),
    "Dropdown": ("microui.advance", "Dropdown"),
    "Avatar": ("microui.advance", "Avatar"),
    "Progress": ("microui.advance", "Progress"),
    "Stats": ("microui.advance", "Stats"),
    "Timeline": ("microui.advance", "Timeline"),
    "Collapse": ("microui.advance", "Collapse"),
    "Divider": ("microui.advance", "Divider"),
    "Toast": ("microui.advance", "Toast"),
    "Pagination": ("microui.advance", "Pagination"),
    "Skeleton": ("microui.advance", "Skeleton"),
    "Tooltip": ("microui.advance", "Tooltip"),
    "Swap": ("microui.advance", "Swap"),
    # Layout components
    "Pricing": ("microui.layout", "Pricing"),
    "Contact": ("microui.layout", "Contact"),
    # Page layouts
    "DashBordLayout": ("microui.layout_pages", "DashBordLayout"),
    "LandingPage": ("microui.layout_pages", "LandingPage"),
    "KanbanLayout": ("microui.layout_pages", "KanbanLayout"),
    "EcommerceLayout": ("microui.layout_pages", "EcommerceLayout"),
    # Pages module
    "LoginConfig": ("microui.pages", "LoginConfig"),
    "RegisterConfig": ("microui.pages", "RegisterConfig"),
    "ProfileConfig": ("microui.pages", "ProfileConfig"),
    "UsersManagementConfig": ("microui.pages", "UsersManagementConfig"),
    "SettingsConfig": ("microui.pages", "SettingsConfig"),
    "AuthComponents": ("microui.pages", "AuthComponents"),
    "AuthPages": ("microui.pages", "AuthPages"),
    "ProfilePages": ("microui.pages", "ProfilePages"),
    "UsersManagement": ("microui.pages", "UsersManagement"),
    "SettingsPages": ("microui.pages", "SettingsPages"),
    # Theme utilities
    "ThemeManager": ("microui.thems", "ThemeManager"),
    "create_theme_routes": ("microui.thems", "create_theme_routes"),
    "get_theme_context": ("microui.thems", "get_theme_context"),
    "register_theme_helpers": ("microui.thems", "register_theme_helpers"),
    "setup_daisy_ui": ("microui.thems", "setup_daisy_ui"),
}


def __getattr__(name: str):
    """Lazy load components on first access"""
    if name in _import_map:
        module_path, attr_name = _import_map[name]
        import importlib
        
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
