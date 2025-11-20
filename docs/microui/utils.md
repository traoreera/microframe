# Utility Helpers

Documentation for utility functions from `microui/utils.py`.

Utility helpers reduce code duplication and provide reusable functions for HTML generation.

## String Building Functions

### build_class_list()

Build a space-separated class string from a list and additional classes.

**Parameters:**
- `base_classes` (List[str]): Base CSS classes
- `additional` (str, default=""): Additional classes to append

**Returns:** `str` - Space-separated class string

**Example:**
```python
from microui.utils import build_class_list

classes = build_class_list(
    ["btn", "btn-primary"],
    "shadow-2xl hover:scale-110"
)
# Result: "btn btn-primary shadow-2xl hover:scale-110"
```

---

### build_hx_attrs()

Build HTMX attributes string from parameters.

**Parameters:**
- `hx_get` (Optional[str]): HTMX GET URL
- `hx_post` (Optional[str]): HTMX POST URL
- `hx_put` (Optional[str]): HTMX PUT URL
- `hx_delete` (Optional[str]): HTMX DELETE URL
- `hx_target` (Optional[str]): HTMX target selector
- `hx_swap` (Optional[str]): HTMX swap strategy
- `hx_trigger` (Optional[str]): HTMX trigger event
- `hx_vals` (Optional[str]): HTMX values (JSON string)

**Returns:** `str` - Space-separated HTMX attributes

**Example:**
```python
from microui.utils import build_hx_attrs

attrs = build_hx_attrs(
    hx_get="/api/data",
    hx_target="#result",
    hx_swap="innerHTML",
    hx_trigger="click"
)
# Result: 'hx-get="/api/data" hx-target="#result" hx-swap="innerHTML" hx-trigger="click"'
```

---

### build_link()

Build an anchor tag with optional HTMX attributes.

**Parameters:**
- `href` (str): Link URL
- `text` (str): Link text
- `classes` (str, default=""): CSS classes
- `hx_get` (Optional[str]): HTMX GET URL
- `hx_target` (Optional[str]): HTMX target
- `hx_swap` (Optional[str]): HTMX swap strategy

**Returns:** `str` - Complete anchor tag HTML

**Example:**
```python
from microui.utils import build_link

link = build_link(
    href="/users",
    text="View Users",
    classes="btn btn-primary",
    hx_get="/api/users",
    hx_target="#content"
)
# Result: '<a href="/users" class="btn btn-primary" hx-get="/api/users" hx-target="#content">View Users</a>'
```

---

## Menu Building Functions

### build_menu_items()

Build menu items HTML from a list of dictionaries.

**Parameters:**
- `items` (List[Dict]): Menu items
  - Each item: `{"text": str, "href": str, "icon": str, "active": bool, "hx_get": Optional[str], "submenu": Optional[List]}`
- `item_classes` (str, default=""): Additional classes for menu items

**Returns:** `str` - Complete menu HTML

**Example:**
```python
from microui.utils import build_menu_items

menu = build_menu_items(
    items=[
        {"text": "Home", "href": "/", "icon": "🏠", "active": True},
        {"text": "Users", "href": "/users", "icon": "👥"},
        {
            "text": "Settings",
            "icon": "⚙️",
            "submenu": [
                {"text": "Profile", "href": "/profile"},
                {"text": "Security", "href": "/security"}
            ]
        }
    ]
)
```

**Output:**
```html
<li>
    <a href="/" class="active">🏠 Home</a>
</li>
<li>
    <a href="/users">👥 Users</a>
</li>
<li>
    <details>
        <summary>⚙️ Settings</summary>
        <ul>
            <li><a href="/profile">Profile</a></li>
            <li><a href="/security">Security</a></li>
        </ul>
    </details>
</li>
```

---

### build_feature_list()

Build a feature list with checkmarks or custom icons.

**Parameters:**
- `features` (List[str]): List of feature descriptions
- `icon` (str, default="✓"): Icon for each feature
- `icon_class` (str, default="text-success"): CSS class for icon

**Returns:** `str` - Feature list HTML

**Example:**
```python
from microui.utils import build_feature_list

features = build_feature_list(
    features=[
        "Unlimited projects",
        "Priority support",
        "100GB storage",
        "API access"
    ],
    icon="✓",
    icon_class="text-success"
)
```

**Output:**
```html
<li class="flex items-center gap-2">
    <span class="text-success">✓</span> Unlimited projects
</li>
<li class="flex items-center gap-2">
    <span class="text-success">✓</span> Priority support
</li>
...
```

---

## SVG Icon Cache

### SVG_ICONS

Dictionary of pre-cached SVG icons for better performance.

**Available Icons:**
- `chevron-down`: Dropdown arrow
- `menu`: Hamburger menu icon
- `close`: Close/X icon

**Example:**
```python
from microui.utils import SVG_ICONS

chevron = SVG_ICONS["chevron-down"]
menu = SVG_ICONS["menu"]
close = SVG_ICONS["close"]
```

---

### get_svg_icon()

Get a cached SVG icon by name.

**Parameters:**
- `name` (str): Icon name

**Returns:** `str` - SVG icon HTML or empty string if not found

**Example:**
```python
from microui.utils import get_svg_icon

icon = get_svg_icon("chevron-down")
# Returns the SVG markup for chevron-down icon
```

---

## Usage in Components

These utilities are used internally by MicroUI components to reduce code duplication.

### Example: Using in Custom Components

```python
from microui.utils import build_class_list, build_hx_attrs, build_feature_list
from markupsafe import Markup

def custom_card(title, features, action_url):
    """Custom card component using utilities"""
    
    classes = build_class_list(
        ["card", "bg-base-100", "shadow-xl"],
        "hover:shadow-2xl transition-shadow"
    )
    
    hx_attrs = build_hx_attrs(
        hx_get=action_url,
        hx_target="#content",
        hx_swap="innerHTML"
    )
    
    features_html = build_feature_list(features)
    
    return Markup(f"""
    <div class="{classes}">
        <div class="card-body">
            <h2 class="card-title">{title}</h2>
            <ul class="space-y-2">
                {features_html}
            </ul>
            <button class="btn btn-primary" {hx_attrs}>
                View Details
            </button>
        </div>
    </div>
    """)

# Usage
card = custom_card(
    title="Premium Plan",
    features=["Feature 1", "Feature 2", "Feature 3"],
    action_url="/plans/premium"
)
```

### Example: Building Dynamic Menus

```python
from microui.utils import build_menu_items

def get_user_menu(user):
    """Build user-specific menu"""
    
    items = [
        {"text": "Dashboard", "href": "/dashboard", "icon": "📊", "active": True}
    ]
    
    if user.is_admin:
        items.append({
            "text": "Admin",
            "icon": "⚙️",
            "submenu": [
                {"text": "Users", "href": "/admin/users"},
                {"text": "Settings", "href": "/admin/settings"}
            ]
        })
    
    return build_menu_items(items)
```

---

## Performance Benefits

Using these utilities provides:

- **Code Reduction**: ~80 lines of duplicated code eliminated
- **Consistency**: Uniform HTML generation across components
- **Maintainability**: Single source of truth for common patterns
- **Performance**: Reusable functions reduce overhead

---

## Best Practices

1. **Use build_hx_attrs()** for all HTMX attribute generation
2. **Use build_class_list()** to merge base and custom classes
3. **Use build_menu_items()** for consistent menu structures
4. **Cache SVG icons** with get_svg_icon() for repeated use
5. **Build feature lists** with build_feature_list() for consistency

---

📚 **[Back to MicroUI Documentation](README.md)**
