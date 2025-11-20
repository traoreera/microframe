# UI Module

Documentation for `microframe/ui/` - Template engine and component system.

## TemplateEngine

Jinja2-based template engine with async support and component system.

### Basic Usage

```python
from microframe.ui import TemplateEngine

# Initialize engine
engine = TemplateEngine(
    directory="templates",
    debug=True,
    cache=False
)

# Render template
@app.get("/page")
async def page(request):
    return await engine.render(
        "page.html",
        ctx={"title": "My Page", "user": user},
        request=request
    )
```

## Configuration

### __init__()

```python
TemplateEngine(
    directory="templates",
    debug=True,
    cache=False
)
```

**Parameters:**
- `directory` (str): Templates directory path
- `debug` (bool): Enable auto-reload on changes
- `cache` (bool): Enable bytecode caching

## Features

### 1. Async Template Rendering

```python
@app.get("/")
async def home(request):
    return await engine.render("home.html", ctx={}, request=request)
```

### 2. HTMX Partial Support

Automatically renders partials for HTMX requests:

```python
# Request with HX-Request header
# Looks for templates/partials/page.html
return await engine.render("page.html", request=request)
```

### 3. Component System

#### ComponentRegistry

Register reusable Jinja2 components.

```python
from microframe.ui import ComponentRegistry

# Register component
ComponentRegistry.register("button", """
<button class="{{ class }}">{{ slot }}</button>
""")
```

#### Auto-Register Components

Automatically register all `.html` files from a directory:

```python
from microframe.ui import auto_register_components

auto_register_components("templates/components")
# Registers: button.html, card.html, etc.
```

#### Using Components in Templates

```jinja2
{% component "button" class="btn btn-primary" %}
    Click Me
{% endcomponent %}
```

### 4. Global Functions

Built-in template functions:

```jinja2
{# Static files #}
<link href="{{ static('css/style.css') }}" rel="stylesheet">

{# URL generation #}
<a href="{{ url('about') }}">About</a>
```

## Helper Functions

### get_engine()

Get singleton instance of TemplateEngine.

```python
from microframe.ui import get_engine

engine = get_engine()
```

### render()

Shorthand for rendering templates.

```python
from microframe.ui import render

@app.get("/")
async def home(request):
    return await render("home.html", {"title": "Home"}, request)
```

### list_templates()

List all available templates.

```python
from microframe.ui import list_templates

templates = list_templates()
# Returns: ['home.html', 'about.html', ...]
```

## Complete Example

### Project Structure

```
project/
├── app.py
└── templates/
    ├── base.html
    ├── home.html
    ├── components/
    │   ├── button.html
    │   └── card.html
    └── partials/
        └── user-list.html
```

### Component: button.html

```html
<button class="btn {{ class|default('btn-primary') }}" {{ attrs|default('') }}>
    {{ slot }}
</button>
```

### Component: card.html

```html
<div class="card {{ class|default('') }}">
    {% if title %}
    <div class="card-header">
        <h3>{{ title }}</h3>
    </div>
    {% endif %}
    <div class="card-body">
        {{ slot }}
    </div>
</div>
```

### Template: base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link href="{{ static('css/style.css') }}" rel="stylesheet">
</head>
<body>
    {% block content %}{% endblock %}
    <script src="{{ static('js/app.js') }}"></script>
</body>
</html>
```

### Template: home.html

```html
{% extends "base.html" %}

{% block content %}
<div class="container">
    <h1>{{ title }}</h1>
    
    {% component "button" class="btn-lg" %}
        Get Started
    {% endcomponent %}
    
    {% component "card" title="Welcome" class="mt-4" %}
        <p>Welcome to our application!</p>
    {% endcomponent %}
</div>
{% endblock %}
```

### Application: app.py

```python
from microframe import Application
from microframe.ui import TemplateEngine

app = Application()
engine = TemplateEngine(directory="templates", cache=True)

@app.get("/")
async def home(request):
    return await engine.render(
        "home.html",
        ctx={"title": "Home Page"},
        request=request
    )

@app.get("/users")
async def users(request):
    # HTMX request automatically gets partial
    users = get_users()
    return await engine.render(
        "user-list.html",
        ctx={"users": users},
        request=request
    )
```

## HTMX Integration

### Automatic Partial Rendering

When a request has the `HX-Request` header, the engine looks for templates in `partials/` directory:

```python
# Regular request: renders templates/page.html
# HTMX request: renders templates/partials/page.html (if exists)

@app.get("/content")
async def content(request):
    return await engine.render("content.html", request=request)
```

### Example with HTMX

**HTML:**
```html
<div id="content">
    <button hx-get="/content" hx-target="#content">
        Load Content
    </button>
</div>
```

**Template (templates/partials/content.html):**
```html
<div class="loaded-content">
    <p>This content was loaded via HTMX!</p>
</div>
```

## Cookie Management

### cookies.py

Cookie utilities for template context.

```python
from microframe.ui import get_cookie, set_cookie

@app.get("/")
async def home(request):
    theme = get_cookie(request, "theme", default="light")
    return await engine.render("home.html", {"theme": theme}, request)

@app.post("/theme")
async def set_theme(request, response):
    data = await request.form()
    set_cookie(response, "theme", data["theme"], max_age=31536000)
    return response
```

## Best Practices

### 1. Use Components for Reusability

```html
<!-- templates/components/alert.html -->
<div class="alert alert-{{ type|default('info') }}">
    {{ slot }}
</div>
```

### 2. Organize Templates

```
templates/
├── layouts/        # Base layouts
│   └── base.html
├── pages/         # Full pages
│   ├── home.html
│   └── about.html
├── components/    # Reusable components
│   ├── button.html
│   └── card.html
└── partials/      # HTMX partials
    └── users.html
```

### 3. Enable Caching in Production

```python
engine = TemplateEngine(
    directory="templates",
    debug=False,  # Disable debug in production
    cache=True    # Enable caching
)
```

### 4. Use Context Processors

```python
def add_global_context(ctx, request):
    ctx["user"] = get_current_user(request)
    ctx["app_name"] = "MyApp"
    return ctx

@app.get("/")
async def home(request):
    ctx = add_global_context({}, request)
    return await engine.render("home.html", ctx, request)
```

## Advanced Features

### Custom Jinja2 Filters

```python
def format_date(value):
    return value.strftime("%Y-%m-%d")

engine.env.filters["date"] = format_date

# Use in template:
# {{ created_at|date }}
```

### Custom Extensions

```python
from jinja2.ext import Extension

class MyExtension(Extension):
    # Custom extension logic
    pass

engine.env.add_extension(MyExtension)
```

---

📚 **[Back to MicroFrame Documentation](README.md)**
