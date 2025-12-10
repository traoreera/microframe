# microui/components/__init__.py
from .alert import Alert
from .avatar import Avatar
from .badge import Badge
from .breadcrumb import Breadcrumb
from .button import Button
from .card import Card
from .checkbox import Checkbox
from .collapse import Collapse
from .divider import Divider
from .drawer import Drawer
from .dropdown import Dropdown
from .footer import Footer
from .input import Input
from .loading import Loading
from .modal import Modal
from .navbar import Navbar
from .pagination import Pagination
from .progress import Progress
from .radio import Radio
from .select import Select
from .sidebar import Sidebar
from .skeleton import Skeleton
from .stats import Stats
from .swap import Swap
from .table import Table
from .tabs import Tabs
from .textarea import Textarea
from .theme_switcher import ThemeSwitcher
from .timeline import Timeline
from .toast import Toast
from .tooltip import Tooltip

__all__ = [
    "Alert",
    "Button",
    "Card",
    "Input",
    "Navbar",
    "Checkbox",
    "Radio",
    "Select",
    "Textarea",
    "ThemeSwitcher",
    "Modal",
    "Table",
    "Badge",
    "Loading",
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
    "Footer",
]


def register_compoments():
    from .alert import Alert
    from .avatar import Avatar
    from .badge import Badge
    from .breadcrumb import Breadcrumb
    from .button import Button
    from .card import Card
    from .checkbox import Checkbox
    from .collapse import Collapse
    from .divider import Divider
    from .drawer import Drawer
    from .dropdown import Dropdown
    from .footer import Footer
    from .input import Input
    from .loading import Loading
    from .modal import Modal
    from .navbar import Navbar
    from .pagination import Pagination
    from .progress import Progress
    from .radio import Radio
    from .select import Select
    from .sidebar import Sidebar
    from .skeleton import Skeleton
    from .stats import Stats
    from .swap import Swap
    from .table import Table
    from .tabs import Tabs
    from .textarea import Textarea
    from .theme_switcher import ThemeSwitcher
    from .timeline import Timeline
    from .toast import Toast
    from .tooltip import Tooltip


print("all components have been registered on app")
