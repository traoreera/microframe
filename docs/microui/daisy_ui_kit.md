# DaisyUI Kit Components

Documentation for basic DaisyUI components from `microui/daisy_ui_kit.py`.

## DaisyUI Class

Theme management and switcher component.

### DaisyUI.theme_switcher()

Creates a theme switcher dropdown with all available DaisyUI themes.

**Parameters:**
- `current_theme` (str, default="light"): Currently active theme
- `position` (str, default="dropdown-end"): Dropdown position

**Available Themes:**
light, dark, cupcake, bumblebee, emerald, corporate, synthwave, retro, cyberpunk, valentine, halloween, garden, forest, aqua, lofi, pastel, fantasy, wireframe, black, luxury, dracula, cmyk, autumn, business, acid, lemonade, night, coffee, winter, dim, nord, sunset

**Example:**
```python
from microui import DaisyUI

switcher = DaisyUI.theme_switcher(current_theme="dark", position="dropdown-end")
```

---

## Button Component

Versatile button component with multiple variants and styles.

### Button.render()

**Parameters:**
- `text` (str): Button text
- `variant` (str, default="primary"): Button style variant
  - Options: primary, secondary, accent, ghost, link, info, success, warning, error, neutral, outline
- `size` (str, default="md"): Button size
  - Options: xs, sm, md, lg
- `outline` (bool, default=False): Outline style
- `wide` (bool, default=False): Wider button
- `block` (bool, default=False): Full width button
- `loading` (bool, default=False): Show loading spinner
- `disabled` (bool, default=False): Disable button
- `hx_get` (Optional[str]): HTMX GET request URL
- `hx_post` (Optional[str]): HTMX POST request URL
- `hx_target` (Optional[str]): HTMX target selector
- `hx_swap` (Optional[str]): HTMX swap strategy
- `onclick` (Optional[str]): JavaScript onclick handler
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Button

# Basic button
Button.render("Click Me", variant="primary")

# Large outlined button
Button.render("Submit", variant="secondary", size="lg", outline=True)

# Full width button
Button.render("Continue", variant="success", block=True)

# With HTMX
Button.render(
    text="Load Data",
    variant="primary",
    hx_get="/api/data",
    hx_target="#result",
    hx_swap="innerHTML"
)

# Loading state
Button.render("Processing...", loading=True, disabled=True)

# Custom classes
Button.render("Custom", classes="shadow-2xl hover:scale-110")
```

---

## Card Component

Container component for displaying content with optional image, title, and actions.

### Card.render()

**Parameters:**
- `title` (Optional[str]): Card title
- `body` (str, default=""): Card body content (HTML)
- `image` (Optional[str]): Image URL
- `actions` (Optional[str]): Action buttons HTML
- `compact` (bool, default=False): Compact card style
- `bordered` (bool, default=False): Add border
- `side` (bool, default=False): Side-by-side layout (image beside content)
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Card, Button

# Basic card
Card.render(
    title="Card Title",
    body="<p>Card content goes here</p>",
    actions=Button.render("Action", variant="primary")
)

# Card with image
Card.render(
    title="Product",
    body="<p>Product description</p>",
    image="https://example.com/product.jpg",
    bordered=True
)

# Compact card
Card.render(
    title="Quick Info",
    body="Brief content",
    compact=True
)

# Side layout
Card.render(
    title="Side Card",
    body="Content beside image",
    image="image.jpg",
    side=True
)
```

---

## Alert Component

Alert/notification component for displaying messages.

### Alert.render()

**Parameters:**
- `message` (str): Alert message
- `type` (str, default="info"): Alert type
  - Options: info, success, warning, error
- `dismissible` (bool, default=False): Add close button
- `icon` (Optional[str]): Custom icon HTML
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Alert

# Different types
Alert.render("Operation successful!", type="success")
Alert.render("Warning message", type="warning")
Alert.render("Error occurred", type="error")
Alert.render("Information", type="info")

# Dismissible
Alert.render("You can close this", type="info", dismissible=True)

# Custom icon
Alert.render("Custom alert", type="success", icon="✓")
```

---

## Modal Component

Dialog/modal component for displaying overlays.

### Modal.render()

**Parameters:**
- `id` (str): Unique modal ID
- `title` (str): Modal title
- `content` (str): Modal body content (HTML)
- `actions` (Optional[str]): Action buttons HTML
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Modal, Button

# Basic modal
modal = Modal.render(
    id="my-modal",
    title="Confirm Action",
    content="<p>Are you sure you want to proceed?</p>",
    actions=f"""
        {Button.render("Cancel", variant="ghost", onclick="my_modal.close()")}
        {Button.render("Confirm", variant="primary")}
    """
)

# Open modal with JavaScript
# <button onclick="my_modal.showModal()">Open Modal</button>
```

---

## Input Component

Form input component with label and validation.

### Input.render()

**Parameters:**
- `name` (str): Input name attribute
- `type` (str, default="text"): Input type (text, email, password, tel, etc.)
- `placeholder` (str, default=""): Placeholder text
- `value` (str, default=""): Input value
- `label` (Optional[str]): Input label
- `size` (str, default="md"): Input size
  - Options: xs, sm, md, lg
- `bordered` (bool, default=True): Show border
- `error` (Optional[str]): Error message
- `hx_post` (Optional[str]): HTMX POST URL
- `hx_trigger` (Optional[str]): HTMX trigger event
- `hx_target` (Optional[str]): HTMX target selector
- `required` (bool, default=True): Required field
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Input

# Basic input
Input.render(
    name="username",
    type="text",
    label="Username",
    placeholder="Enter username",
    required=True
)

# Email input
Input.render(
    name="email",
    type="email",
    label="Email Address",
    placeholder="you@example.com"
)

# With error
Input.render(
    name="email",
    type="email",
    label="Email",
    error="Invalid email format"
)

# With HTMX validation
Input.render(
    name="username",
    label="Username",
    hx_post="/validate/username",
    hx_trigger="blur",
    hx_target="#validation-result"
)
```

---

## Table Component

Data table component with optional zebra stripes and hover effects.

### Table.render()

**Parameters:**
- `headers` (List[str]): Table header labels
- `rows` (List[List[str]]): Table rows (each row is a list of cell values)
- `zebra` (bool, default=False): Zebra striping
- `compact` (bool, default=False): Compact table style
- `hoverable` (bool, default=True): Highlight row on hover
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Table, Badge

# Basic table
Table.render(
    headers=["ID", "Name", "Email", "Status"],
    rows=[
        ["1", "Alice", "alice@example.com", "Active"],
        ["2", "Bob", "bob@example.com", "Inactive"],
    ],
    zebra=True,
    hoverable=True
)

# With components in cells
Table.render(
    headers=["User", "Role", "Actions"],
    rows=[
        ["Alice", Badge.render("Admin", variant="primary"), "<button>Edit</button>"],
        ["Bob", Badge.render("User", variant="neutral"), "<button>Edit</button>"],
    ]
)
```

---

## Badge Component

Small badge component for labels and status indicators.

### Badge.render()

**Parameters:**
- `text` (str): Badge text
- `variant` (str, default="neutral"): Badge color variant
  - Options: primary, secondary, accent, ghost, info, success, warning, error, neutral
- `size` (str, default="md"): Badge size
  - Options: xs, sm, md, lg
- `outline` (bool, default=False): Outline style
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Badge

# Different variants
Badge.render("New", variant="primary")
Badge.render("Success", variant="success")
Badge.render("Warning", variant="warning")
Badge.render("Error", variant="error")

# Sizes
Badge.render("Small", size="sm")
Badge.render("Large", size="lg")

# Outline
Badge.render("Outline", variant="primary", outline=True)
```

---

## Navbar Component

Navigation bar component.

### Navbar.render()

**Parameters:**
- `brand` (str): Brand name/logo
- `items` (List[dict]): Navigation items
  - Each item: `{"text": str, "href": str, "hx_get": Optional[str]}`
- `end_items` (Optional[str]): HTML content for navbar end section
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Navbar, DaisyUI

# Basic navbar
Navbar.render(
    brand="My App",
    items=[
        {"text": "Home", "href": "/"},
        {"text": "About", "href": "/about"},
        {"text": "Contact", "href": "/contact"}
    ]
)

# With theme switcher
Navbar.render(
    brand="My App",
    items=[
        {"text": "Dashboard", "hx_get": "/dashboard"},
        {"text": "Settings", "href": "/settings"}
    ],
    end_items=DaisyUI.theme_switcher()
)
```

---

## Loading Component

Loading spinner/indicator component.

### Loading.render()

**Parameters:**
- `type` (str, default="spinner"): Loading animation type
  - Options: spinner, dots, ring, ball, bars, infinity
- `size` (str, default="md"): Loading indicator size
  - Options: xs, sm, md, lg
- `color` (Optional[str]): Color (primary, secondary, accent, etc.)
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Examples:**
```python
from microui import Loading

# Different types
Loading.render(type="spinner", size="md")
Loading.render(type="dots", size="lg")
Loading.render(type="ring", size="sm", color="primary")
Loading.render(type="ball", color="secondary")
Loading.render(type="bars", color="accent")
```

---

## Helper Functions

### register_components()

Returns a dictionary of all registered components for template usage.

**Returns:** `dict` - Component render functions keyed by name

**Example:**
```python
from microui import register_components

components = register_components()
# Use in Jinja2 templates
# {{ button("Click", variant="primary") }}
```

---

📚 **[Back to MicroUI Documentation](README.md)**
