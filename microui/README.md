# MicroUI

> DaisyUI components for Python/HTMX - Build beautiful, responsive web interfaces with Python

MicroUI is a comprehensive Python library that brings DaisyUI components to your Python web applications. Perfect for use with HTMX, it provides a wide range of pre-built, customizable UI components and full page layouts.

## ✨ Features

- 🎨 **50+ DaisyUI Components** - Buttons, cards, modals, forms, and more
- 🚀 **Lazy Loading** - Components load on-demand for ~60% faster startup
- 📱 **Fully Responsive** - Mobile-first, responsive designs
- 🎭 **30+ Themes** - Built-in DaisyUI theme support with easy switching
- 🔧 **HTMX Ready** - Seamless integration with HTMX attributes
- 📦 **Zero JavaScript** - Pure Python, server-rendered components
- 🎯 **Type Safe** - Full type hints support
- 🏗️ **Page Layouts** - Ready-to-use dashboard, landing page, kanban, and e-commerce layouts

## 📦 Installation

```bash
# MicroUI is included with MicroFrame
pip install microframe
```

## 🚀 Quick Start

### Basic Component Usage

```python
from microframe import Application
from microui import Button, Card, Alert

app = Application()

@app.get("/")
async def home():
    return f"""
    <!DOCTYPE html>
    <html data-theme="dark">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css" rel="stylesheet" />
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        <div class="container mx-auto p-8">
            {Alert.render("Welcome to MicroUI!", type="success")}
            
            {Card.render(
                title="Hello World",
                body="This is a beautiful card component",
                actions=Button.render("Click Me", variant="primary")
            )}
        </div>
    </body>
    </html>
    """
```

### Using Full Page Layouts

```python
from microui import LandingPage

@app.get("/")
async def landing():
    return LandingPage.render(
        title="My App",
        hero_title="Build Amazing Apps",
        hero_subtitle="With Python and MicroUI",
        features=[
            {"icon": "⚡", "title": "Fast", "desc": "Lightning fast performance"},
            {"icon": "🎨", "title": "Beautiful", "desc": "Stunning UI components"},
        ]
    )
```

## 📚 Component Categories

### Basic Components
- **Button**, **Card**, **Alert**, **Modal**, **Input**, **Table**
- **Badge**, **Navbar**, **Loading**

### Advanced Components  
- **Sidebar**, **Drawer**, **Breadcrumb**, **Tabs**, **Dropdown**
- **Avatar**, **Progress**, **Stats**, **Timeline**, **Collapse**
- **Toast**, **Pagination**, **Skeleton**, **Tooltip**

### Layout Components
- **Pricing** - Pricing tables and cards
- **Contact** - Contact forms and pages

### Page Layouts
- **DashBordLayout** - Complete dashboard with sidebar
- **LandingPage** - Landing page with hero, features, pricing
- **KanbanLayout** - Kanban board layout
- **EcommerceLayout** - E-commerce page layout

### Authentication & User Pages
- **AuthPages** - Login, register, forgot password pages
- **ProfilePages** - User profile pages
- **UsersManagement** - User management pages
- **SettingsPages** - Settings pages
- **Config Classes** - LoginConfig, RegisterConfig, ProfileConfig, etc.

## 💡 Usage Examples

### Creating a Dashboard

```python
from microui import DashBordLayout, Stats

@app.get("/dashboard")
async def dashboard():
    content = f"""
    {Stats.render([
        {"title": "Users", "value": "1,234", "icon": "👥", "color": "primary"},
        {"title": "Sales", "value": "$5,678", "icon": "💰", "color": "success"},
    ])}
    """
    
    return DashBordLayout.render(
        title="Dashboard",
        sidebar_items=[
            {"text": "Overview", "href": "/dashboard", "icon": "📊", "active": True},
            {"text": "Analytics", "href": "/analytics", "icon": "📈"},
        ],
        content=content,
        user_name="John Doe"
    )
```

### HTMX Integration

```python
from microui import Button

@app.get("/")
async def home():
    return f"""
    {Button.render(
        text="Load Data",
        hx_get="/api/data",
        hx_target="#result",
        hx_swap="innerHTML"
    )}
    <div id="result"></div>
    """

@app.get("/api/data")
async def get_data():
    return "<p>Data loaded via HTMX!</p>"
```

### Theme Switching

```python
from microui import DaisyUI

navbar = f"""
<div class="navbar bg-base-100">
    <div class="navbar-end">
        {DaisyUI.theme_switcher(current_theme="dark")}
    </div>
</div>
"""
```

### Authentication Pages

```python
from microui import AuthPages, LoginConfig

@app.get("/login")
async def login():
    config = LoginConfig(
        form_action="/auth/login",
        title="Welcome Back",
        logo="🔐"
    )
    return AuthPages.login_page(config)

@app.get("/register")
async def register():
    return AuthPages.register_page()
```

## 🏗️ Module Structure

```
microui/
├── __init__.py          # Lazy loading exports
├── daisy_ui_kit.py      # Basic DaisyUI components
├── advance.py           # Advanced components
├── layout.py            # Layout components (735 lines)
├── layout_pages.py      # Full page layouts
├── pages/               # Authentication & user pages
│   ├── authpage.py      # Login, register, forgot password
│   ├── profilePage.py   # User profile pages
│   ├── userManager.py   # User management
│   └── settings.py      # Settings pages
├── utils.py             # Utility helpers
└── thems.py            # Theme management
```

## ⚡ Performance

- **Lazy imports**: ~60% faster startup
- **Optimized rendering**: Efficient HTML generation
- **Code reduction**: ~80 lines eliminated through utilities
- **File organization**: 39% reduction in largest file

## 🎨 Available Themes

`light`, `dark`, `cupcake`, `bumblebee`, `emerald`, `corporate`, `synthwave`, `retro`, `cyberpunk`, `valentine`, `halloween`, `garden`, `forest`, `aqua`, `lofi`, `pastel`, `fantasy`, `wireframe`, `black`, `luxury`, `dracula`, `cmyk`, `autumn`, `business`, `acid`, `lemonade`, `night`, `coffee`, `winter`, `dim`, `nord`, `sunset`

## 📖 Documentation

For more detailed documentation:
- [MicroFrame Main Docs](../docs/)
- [Component API Reference](../docs/microui/)

## 🤝 Contributing

MicroUI is part of the MicroFrame project. Contributions are welcome!

## 📄 License

MicroUI is part of MicroFrame and shares the same license.

## 🙏 Acknowledgements

- Built on [DaisyUI](https://daisyui.com/) design system
- Powered by [Tailwind CSS](https://tailwindcss.com/)
- Designed for [HTMX](https://htmx.org/) integration

---

Made with ❤️ for the Python community
