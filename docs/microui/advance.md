# Advanced Components

Documentation for advanced DaisyUI components from `microui/advance.py`.

## Sidebar Component

Collapsible sidebar navigation with menu items and optional submenu support.

### Sidebar.render()

**Parameters:**
- `items` (List[Dict]): Menu items
  - Each item: `{"text": str, "href": str, "icon": str, "active": bool, "hx_get": Optional[str], "submenu": Optional[List[Dict]]}`
- `brand` (Optional[str]): Brand name
- `brand_logo` (Optional[str]): Brand logo URL
- `footer` (Optional[str]): Footer content HTML
- `compact` (bool, default=False): Compact sidebar (icons only)
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Sidebar

sidebar = Sidebar.render(
    items=[
        {"text": "Dashboard", "href": "/", "icon": "📊", "active": True},
        {"text": "Users", "href": "/users", "icon": "👥"},
        {
            "text": "Settings",
            "icon": "⚙️",
            "submenu": [
                {"text": "Profile", "href": "/profile"},
                {"text": "Security", "href": "/security"}
            ]
        }
    ],
    brand="My App",
    brand_logo="logo.png",
    footer="<p>© 2024</p>"
)
```

---

## Drawer Component

Responsive drawer component for sidebar layouts.

### Drawer.render()

**Parameters:**
- `sidebar_content` (str): Sidebar HTML content
- `main_content` (str): Main content HTML
- `drawer_id` (str, default="sidebar-drawer"): Drawer ID
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Drawer, Sidebar

sidebar = Sidebar.render(items=[...])
content = "<div>Main content</div>"

layout = Drawer.render(
    sidebar_content=sidebar,
    main_content=content
)
```

---

## Breadcrumb Component

Navigation breadcrumb component.

### Breadcrumb.render()

**Parameters:**
- `items` (List[Dict]): Breadcrumb items
  - Each item: `{"text": str, "href": str}`
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Breadcrumb

breadcrumb = Breadcrumb.render(
    items=[
        {"text": "Home", "href": "/"},
        {"text": "Products", "href": "/products"},
        {"text": "Details"}  # Last item has no href
    ]
)
```

---

## Tabs Component

Tabbed interface component.

### Tabs.render()

**Parameters:**
- `tabs` (List[Dict]): Tab items
  - Each tab: `{"id": str, "text": str, "content": str, "active": bool}`
- `variant` (str, default="bordered"): Tab style
  - Options: bordered, lifted, boxed
- `size` (str, default="md"): Tab size
  - Options: xs, sm, md, lg
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Tabs

tabs = Tabs.render(
    tabs=[
        {"id": "tab1", "text": "Overview", "content": "<p>Overview content</p>", "active": True},
        {"id": "tab2", "text": "Details", "content": "<p>Details content</p>"},
        {"id": "tab3", "text": "Settings", "content": "<p>Settings content</p>"}
    ],
    variant="lifted",
    size="md"
)
```

---

## Dropdown Component

Dropdown menu component.

### Dropdown.render()

**Parameters:**
- `button_text` (str): Dropdown button text
- `items` (List[Dict]): Menu items
  - Each item: `{"text": str, "href": str, "icon": str, "hx_get": Optional[str], "divider": bool}`
- `position` (str, default="dropdown-end"): Dropdown position
  - Options: dropdown-end, dropdown-top, dropdown-bottom, dropdown-left, dropdown-right
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Dropdown

dropdown = Dropdown.render(
    button_text="Actions",
    items=[
        {"text": "Edit", "href": "/edit", "icon": "✏️"},
        {"text": "Delete", "href": "/delete", "icon": "🗑️"},
        {"divider": True},
        {"text": "Settings", "href": "/settings", "icon": "⚙️"}
    ],
    position="dropdown-end"
)
```

---

## Avatar Component

User avatar component with online/offline status.

### Avatar.render()

**Parameters:**
- `src` (str): Avatar image URL
- `alt` (str, default="Avatar"): Alt text
- `size` (str, default="md"): Avatar size
  - Options: xs, sm, md, lg, xl
- `shape` (str, default="circle"): Avatar shape
  - Options: circle, square
- `online` (bool, default=False): Show online indicator
- `offline` (bool, default=False): Show offline indicator
- `placeholder` (Optional[str]): Placeholder text (for initials)
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Avatar

# Image avatar
Avatar.render(
    src="avatar.jpg",
    size="md",
    shape="circle",
    online=True
)

# Placeholder avatar (initials)
Avatar.render(
    src="",
    placeholder="JD",
    size="lg"
)
```

---

## Progress Component

Progress bar component.

### Progress.render()

**Parameters:**
- `value` (int): Progress value
- `max` (int, default=100): Maximum value
- `color` (Optional[str]): Progress bar color (primary, secondary, accent, success, warning, error)
- `size` (str, default="md"): Progress bar size
  - Options: xs, sm, md, lg
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Progress

Progress.render(value=75, max=100, color="primary", size="md")
Progress.render(value=50, color="success")
```

---

## Stats Component

Statistics display component.

### Stats.render()

**Parameters:**
- `stats` (List[Dict]): Statistics items
  - Each stat: `{"title": str, "value": str, "desc": str, "icon": str, "color": str}`
- `vertical` (bool, default=False): Vertical orientation
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Stats

stats = Stats.render([
    {
        "title": "Total Users",
        "value": "1,234",
        "desc": "+12% this month",
        "icon": "👥",
        "color": "primary"
    },
    {
        "title": "Revenue",
        "value": "$5,678",
        "desc": "+23% this month",
        "icon": "💰",
        "color": "success"
    }
])
```

---

## Timeline Component

Event timeline component.

### Timeline.render()

**Parameters:**
- `items` (List[Dict]): Timeline items
  - Each item: `{"title": str, "content": str, "date": str, "icon": str}`
- `compact` (bool, default=False): Compact style
- `snap` (bool, default=False): Snap to icon
- `vertical` (bool, default=True): Vertical orientation
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Timeline

timeline = Timeline.render(
    items=[
        {
            "title": "Project Started",
            "content": "Initial commit",
            "date": "2024-01-01",
            "icon": "✓"
        },
        {
            "title": "First Release",
            "content": "v1.0.0 released",
            "date": "2024-02-01"
        }
    ],
    vertical=True
)
```

---

## Collapse Component

Collapsible/Accordion component.

### Collapse.render()

**Parameters:**
- `items` (List[Dict]): Collapse items
  - Each item: `{"title": str, "content": str, "open": bool}`
- `arrow` (bool, default=True): Show arrow icon
- `plus` (bool, default=False): Show plus icon
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Collapse

collapse = Collapse.render(
    items=[
        {"title": "Question 1", "content": "Answer 1", "open": True},
        {"title": "Question 2", "content": "Answer 2"},
        {"title": "Question 3", "content": "Answer 3"}
    ],
    arrow=True
)
```

---

## Divider Component

Visual divider with optional text.

### Divider.render()

**Parameters:**
- `text` (Optional[str]): Divider text
- `vertical` (bool, default=False): Vertical orientation
- `color` (Optional[str]): Divider color
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Divider

Divider.render()  # Simple divider
Divider.render(text="OR")  # Divider with text
Divider.render(vertical=True)  # Vertical divider
```

---

## Toast Component

Toast notification component.

### Toast.render()

**Parameters:**
- `message` (str): Toast message
- `type` (str, default="info"): Toast type
  - Options: info, success, warning, error
- `position` (str, default="top-end"): Toast position
  - Options: top-start, top-center, top-end, middle-start, middle-center, middle-end, bottom-start, bottom-center, bottom-end
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Toast

Toast.render("Operation successful!", type="success", position="top-end")
Toast.render("Warning message", type="warning", position="bottom-center")
```

---

## Pagination Component

Pagination navigation component.

### Pagination.render()

**Parameters:**
- `current_page` (int): Current page number
- `total_pages` (int): Total number of pages
- `base_url` (str): Base URL for pagination links
- `size` (str, default="md"): Pagination size
  - Options: xs, sm, md, lg
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Pagination

pagination = Pagination.render(
    current_page=3,
    total_pages=10,
    base_url="/products",
    size="md"
)
```

---

## Skeleton Component

Loading skeleton placeholder component.

### Skeleton.render()

**Parameters:**
- `type` (str, default="text"): Skeleton type
  - Options: text, avatar, card, custom
- `lines` (int, default=3): Number of text lines (for text type)
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Skeleton

Skeleton.render(type="text", lines=3)  # Text skeleton
Skeleton.render(type="avatar")  # Avatar skeleton
Skeleton.render(type="card")  # Card skeleton
```

---

## Tooltip Component

Tooltip component for hover information.

### Tooltip.render()

**Parameters:**
- `content` (str): Element content (HTML)
- `text` (str): Tooltip text
- `position` (str, default="top"): Tooltip position
  - Options: top, bottom, left, right
- `color` (Optional[str]): Tooltip color
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Tooltip, Button

tooltip = Tooltip.render(
    content=Button.render("Hover Me"),
    text="This is a tooltip",
    position="top"
)
```

---

## Swap Component

Swap/toggle component for icon switching.

### Swap.render()

**Parameters:**
- `on_icon` (str): Icon when active (HTML)
- `off_icon` (str): Icon when inactive (HTML)
- `rotate` (bool, default=False): Rotate animation
- `flip` (bool, default=False): Flip animation
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Swap

Swap.render(
    on_icon="🌙",
    off_icon="☀️",
    rotate=True
)
```

---

📚 **[Back to MicroUI Documentation](README.md)**
