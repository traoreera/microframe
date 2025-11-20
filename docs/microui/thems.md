# Theme Management

Documentation for theme management from `microui/thems.py`.

## ThemeManager

Manages theme state and persistence for the application.

### ThemeManager.get_theme()

Get the current theme from the request.

**Parameters:**
- `request` (Request): Starlette request object

**Returns:** `str` - Current theme name (default: "light")

**Example:**
```python
from microui import ThemeManager

@app.get("/page")
async def page(request):
    current_theme = ThemeManager.get_theme(request)
    # Use theme in rendering...
    return f'<html data-theme="{current_theme}">'
```

---

### ThemeManager.set_theme()

Set the theme in the request state or cookies.

**Parameters:**
- `request` (Request): Starlette request object
- `theme` (str): Theme name to set

**Returns:** `None`

**Example:**
```python
@app.post("/api/theme/set")
async def set_theme(request):
    data = await request.form()
    ThemeManager.set_theme(request, data["theme"])
    return {"status": "success"}
```

---

### ThemeManager.get_available_themes()

Get list of all available DaisyUI themes.

**Returns:** `List[str]` - List of theme names

**Example:**
```python
@app.get("/api/themes")
async def get_themes():
    themes = ThemeManager.get_available_themes()
    return {"themes": themes}
```

**Available Themes:**
```python
[
    "light", "dark", "cupcake", "bumblebee", "emerald",
    "corporate", "synthwave", "retro", "cyberpunk", "valentine",
    "halloween", "garden", "forest", "aqua", "lofi",
    "pastel", "fantasy", "wireframe", "black", "luxury",
    "dracula", "cmyk", "autumn", "business", "acid",
    "lemonade", "night", "coffee", "winter", "dim",
    "nord", "sunset"
]
```

---

## Helper Functions

### get_theme_context()

Get theme-related context for template rendering.

**Parameters:**
- `request` (Request): Starlette request object

**Returns:** `Dict` - Context dictionary with theme information

**Example:**
```python
from microui import get_theme_context

@app.get("/page")
async def page(request):
    theme_ctx = get_theme_context(request)
    # theme_ctx = {
    #     "current_theme": "dark",
    #     "available_themes": [...],
    #     "is_dark_mode": True
    # }
    
    # Use in templates
    return template.render("page.html", theme_ctx)
```

---

### register_theme_helpers()

Register theme-related Jinja2 template filters and functions.

**Parameters:**
- `env` (Environment): Jinja2 environment

**Returns:** `None`

**Example:**
```python
from jinja2 import Environment
from microui import register_theme_helpers

env = Environment()
register_theme_helpers(env)

# Now you can use theme helpers in templates:
# {{ get_current_theme() }}
# {{ is_dark_theme() }}
```

---

### create_theme_routes()

Create theme management routes to add to your router.

**Parameters:**
- `router` (Router): MicroFrame router instance

**Returns:** `None` - Routes are added to the router

**Example:**
```python
from microframe import Router
from microui import create_theme_routes

router = Router(prefix="/api")
create_theme_routes(router)

# This adds the following routes:
# GET  /api/theme         - Get current theme
# POST /api/theme/set     - Set theme
# GET  /api/themes        - List all themes
```

---

### setup_daisy_ui()

Complete DaisyUI setup including theme routes and helpers.

**Parameters:**
- `app` (Application): MicroFrame application
- `router` (Optional[Router]): Optional router for theme routes

**Returns:** `None`

**Example:**
```python
from microframe import Application, Router
from microui import setup_daisy_ui

app = Application()
router = Router()

# Setup everything
setup_daisy_ui(app=app, router=router)

# This:
# 1. Adds theme routes to router
# 2. Registers template helpers
# 3. Sets up middleware (if needed)
```

---

## Usage Examples

### Complete Theme Integration

```python
from microframe import Application, Router
from microui import setup_daisy_ui, DaisyUI, ThemeManager

app = Application()
router = Router(prefix="/api")

# Setup theme management
setup_daisy_ui(app=app, router=router)

@app.get("/")
async def home(request):
    theme = ThemeManager.get_theme(request)
    
    return f"""
    <!DOCTYPE html>
    <html data-theme="{theme}">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css" rel="stylesheet" />
    </head>
    <body>
        <div class="navbar">
            <div class="navbar-end">
                {DaisyUI.theme_switcher(current_theme=theme)}
            </div>
        </div>
        
        <div class="container mx-auto p-8">
            <h1>Current Theme: {theme}</h1>
        </div>
    </body>
    </html>
    """

app.include_router(router)
```

---

### Theme Switcher in Navbar

```python
from microui import DaisyUI, ThemeManager

@app.get("/page")
async def page(request):
    theme = ThemeManager.get_theme(request)
    
    navbar = f"""
    <div class="navbar bg-base-100">
        <div class="navbar-start">
            <a class="btn btn-ghost text-xl">MyApp</a>
        </div>
        <div class="navbar-end">
            {DaisyUI.theme_switcher(current_theme=theme, position="dropdown-end")}
        </div>
    </div>
    """
    
    return navbar
```

---

### Theme Persistence with Cookies

```python
from starlette.responses import Response

@app.post("/theme/change")
async def change_theme(request):
    data = await request.form()
    theme = data["theme"]
    
    # Set in request state
    ThemeManager.set_theme(request, theme)
    
    # Also set in cookie for persistence
    response = Response("Theme updated")
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=365 * 24 * 60 * 60  # 1 year
    )
    
    return response

@app.get("/page")
async def page(request):
    # Read from cookie if available
    theme = request.cookies.get("theme", "light")
    ThemeManager.set_theme(request, theme)
    
    # Render with theme
    return render_page(theme)
```

---

### Dynamic Theme Preview

```python
from microui import ThemeManager

@app.get("/theme-preview")
async def theme_preview():
    themes = ThemeManager.get_available_themes()
    
    preview_html = ""
    for theme in themes:
        preview_html += f"""
        <div data-theme="{theme}" class="p-4 border rounded mb-4">
            <h3 class="text-xl font-bold mb-2">{theme}</h3>
            <button class="btn btn-primary">Primary</button>
            <button class="btn btn-secondary">Secondary</button>
            <button class="btn btn-accent">Accent</button>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/daisyui@4/dist/full.min.css" rel="stylesheet" />
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        <div class="container mx-auto p-8">
            <h1 class="text-3xl font-bold mb-8">Theme Preview</h1>
            {preview_html}
        </div>
    </body>
    </html>
    """
```

---

### Theme-Aware Components

```python
from microui import ThemeManager, Button, Card

@app.get("/themed-page")
async def themed_page(request):
    theme = ThemeManager.get_theme(request)
    is_dark = theme in ["dark", "dracula", "night", "forest", "black"]
    
    # Render different content based on theme
    if is_dark:
        return Card.render(
            title="Dark Mode Active",
            body="You're viewing the dark theme",
            classes="bg-base-300"
        )
    else:
        return Card.render(
            title="Light Mode Active",
            body="You're viewing the light theme",
            classes="bg-base-100"
        )
```

---

## Client-Side Theme Switching

For immediate visual feedback, combine server-side with client-side:

```html
<script>
function setTheme(theme) {
    // Update DOM immediately
    document.documentElement.setAttribute('data-theme', theme);
    
    // Save to server
    fetch('/api/theme/set', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({theme: theme})
    });
    
    // Save to localStorage
    localStorage.setItem('theme', theme);
}

// Load theme on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
});
</script>
```

---

## Best Practices

1. **Always set data-theme** on `<html>` element
2. **Use ThemeManager** for consistent theme access
3. **Persist theme** in cookies or localStorage
4. **Provide theme switcher** in navigation
5. **Test with multiple themes** during development
6. **Consider system preference** as default:

```javascript
// Detect system theme preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const defaultTheme = prefersDark ? 'dark' : 'light';
```

7. **Support theme in all layouts**:

```python
# Always include theme in layout
def render_layout(request, content):
    theme = ThemeManager.get_theme(request)
    return f"""
    <!DOCTYPE html>
    <html data-theme="{theme}">
    ...
    </html>
    """
```

---

📚 **[Back to MicroUI Documentation](README.md)**
