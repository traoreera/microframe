# MicroUI Documentation

Complete guide to using MicroUI components in your MicroFrame applications.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Component Reference](#component-reference)
5. [Page Layouts](#page-layouts)
6. [Theme Management](#theme-management)
7. [HTMX Integration](#htmx-integration)
8. [Best Practices](#best-practices)

## Introduction

MicroUI is a comprehensive DaisyUI component library for Python/HTMX applications. It provides 50+ pre-built components, full page layouts, and a powerful theme system - all rendered server-side with Python.

### Key Features

- 🎨 **50+ Components** - From basic buttons to complex layouts
- 🚀 **Lazy Loading** - 60% faster startup time
- 📱 **Responsive** - Mobile-first design
- 🎭 **30+ Themes** - DaisyUI theme support
- 🔧 **HTMX Ready** - Built-in HTMX attributes
- 📦 **Zero JavaScript** - Server-rendered
- 🎯 **Type Safe** - Full type hints

## Installation

MicroUI is included with MicroFrame:

```bash
pip install microframe
```

## Quick Start

### Basic Components

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
        <script src="https://unpkg.com/htmx.org@2.0.3"></script>
    </head>
    <body class="p-8">
        {Alert.render("Welcome!", type="success")}
        {Card.render(
            title="Getting Started",
            body="Build beautiful UIs with Python",
            actions=Button.render("Learn More", variant="primary")
        )}
    </body>
    </html>
    """
```

### Full Page Layout

```python
from microui import LandingPage

@app.get("/")
async def landing():
    return LandingPage.render(
        title="My App",
        hero_title="Build Amazing Apps",
        hero_subtitle="With Python and MicroUI",
        features=[
            {"icon": "⚡", "title": "Fast", "desc": "Lightning fast"},
            {"icon": "🎨", "title": "Beautiful", "desc": "Stunning UI"},
        ]
    )
```

## Component Categories

### Basic Components
**Button**, **Card**, **Alert**, **Modal**, **Input**, **Table**, **Badge**, **Navbar**, **Loading**

### Advanced Components  
**Sidebar**, **Drawer**, **Tabs**, **Dropdown**, **Avatar**, **Progress**, **Stats**, **Timeline**, **Toast**, **Pagination**

### Layout Components
**Pricing**, **Contact**

### Page Layouts
**DashBordLayout**, **LandingPage**, **KanbanLayout**, **EcommerceLayout**

### Authentication Pages
**AuthPages**, **ProfilePages**, **UsersManagement**, **SettingsPages**

## Component Examples

### Button

```python
from microui import Button

# Basic
Button.render("Click Me", variant="primary")

# With HTMX
Button.render(
    text="Load Data",
    hx_get="/api/data",
    hx_target="#result"
)

# Variants: primary, secondary, accent, ghost, success, warning, error
# Sizes: xs, sm, md, lg
```

### Dashboard Example

```python
from microui import DashBordLayout, Stats

@app.get("/dashboard")
async def dashboard():
    content = f"""
    {Stats.render([
        {"title": "Users", "value": "1,234", "icon": "👥"},
        {"title": "Revenue", "value": "$5K", "icon": "💰"},
    ])}
    """
    
    return DashBordLayout.render(
        title="Dashboard",
        sidebar_items=[
            {"text": "Overview", "href": "/", "icon": "📊", "active": True},
            {"text": "Settings", "href": "/settings", "icon": "⚙️"}
        ],
        content=content,
        user_name="John Doe"
    )
```

### Authentication

```python
from microui import AuthPages, LoginConfig

@app.get("/login")
async def login():
    return AuthPages.login_page(
        LoginConfig(
            form_action="/auth/login",
            title="Welcome Back",
            logo="🔐"
        )
    )
```

## Theme Management

```python
from microui import DaisyUI, ThemeManager

# Theme switcher
switcher = DaisyUI.theme_switcher(current_theme="dark")

# Get current theme
theme = ThemeManager.get_theme(request)
```

**Available themes:** light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset

## HTMX Integration

All components support HTMX attributes:

```python
Button.render(
    "Load More",
    hx_get="/api/items",
    hx_target="#list",
    hx_swap="beforeend"
)

Input.render(
    name="search",
    hx_post="/search",
    hx_trigger="keyup changed delay:500ms",
    hx_target="#results"
)
```

## Best Practices

### 1. Combine Components

```python
from microui import Card, Button, Badge

def user_card(user):
    return Card.render(
        title=f"{user['name']} {Badge.render(user['role'])}",
        body=user['bio'],
        actions=Button.render("View Profile", variant="primary")
    )
```

### 2. Use Lazy Loading

Components load on-demand automatically - no configuration needed!

### 3. Custom Styling

```python
Button.render(
    "Custom",
    classes="shadow-2xl hover:scale-110"
)
```

### 4. Reusable Components

```python
def success_alert(message):
    return Alert.render(message, type="success", dismissible=True)
```

## Performance

- ⚡ **60% faster startup** - Lazy component loading
- ⚡ **80+ lines reduced** - Utility helpers
- ⚡ **39% file reduction** - Optimized code organization
- ⚡ **Efficient rendering** - Fast HTML generation

## Module Structure

```
microui/
├── __init__.py          # Lazy loading
├── daisy_ui_kit.py      # Basic components
├── advance.py           # Advanced components
├── layout.py            # Layout components
├── layout_pages.py      # Page layouts
├── pages/               # Auth pages
├── utils.py             # Helpers
└── thems.py            # Theme management
```

## API Reference

For complete parameter details, see each component's docstring:

```python
from microui import Button
help(Button.render)
```

## Examples

See the [examples](../../examples/) directory for complete working examples.

## Troubleshooting

**Components not showing?** Include DaisyUI CSS:
```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css" rel="stylesheet" />
```

**HTMX not working?** Include HTMX script:
```html
<script src="https://unpkg.com/htmx.org@2.0.3"></script>
```

---

📚 **[Back to Main Documentation](../../README.md)** | **[MicroUI Source](../../microui/)**
