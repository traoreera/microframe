# Page Layouts

Documentation for full page layouts from `microui/layout_pages.py`.

## DashBordLayout

Complete dashboard layout with sidebar navigation, navbar, and main content area.

### DashBordLayout.render()

**Parameters:**
- `title` (str): Page title
- `sidebar_items` (List[Dict]): Sidebar menu items
  - Each item: `{"text": str, "href": str, "icon": str, "active": bool, "hx_get": Optional[str], "submenu": Optional[List]}`
- `content` (Markup): Main content HTML
- `notifications_count` (int, default=0): Number of notifications
- `theme` (str, default="light"): Theme name
- `avatar` (str, default=""): User avatar URL
- `user_name` (str, default=""): User name

**Returns:** `Markup` - Complete dashboard page HTML

**Example:**
```python
from microui import DashBordLayout, Card, Stats

@app.get("/dashboard")
async def dashboard():
    # Build content
    content = f"""
    {Stats.render([
        {"title": "Total Users", "value": "1,234", "icon": "👥", "color": "primary"},
        {"title": "Revenue", "value": "$5,678", "icon": "💰", "color": "success"},
        {"title": "Orders", "value": "890", "icon": "📦", "color": "info"}
    ])}
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
        {Card.render(title="Recent Activity", body="Activity content...")}
        {Card.render(title="Statistics", body="Stats content...")}
    </div>
    """
    
    return DashBordLayout.render(
        title="Dashboard",
        sidebar_items=[
            {"text": "Overview", "href": "/dashboard", "icon": "📊", "active": True},
            {"text": "Analytics", "href": "/analytics", "icon": "📈"},
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
        content=content,
        user_name="John Doe",
        avatar="avatar.jpg",
        notifications_count=3,
        theme="dark"
    )
```

---

## LandingPage

Complete landing page with hero section, features, pricing, and contact.

### LandingPage.render()

**Parameters:**
- `title` (str): Page/app title
- `hero_title` (str): Hero section title
- `hero_subtitle` (str): Hero section subtitle
- `cta_text` (str, default="Commencer"): Call-to-action button text
- `cta_link` (str, default="/register"): CTA button link
- `features` (List[Dict], default=None): Feature items
  - Each feature: `{"icon": str, "title": str, "desc": str, "image": Optional[str]}`
- `pricing` (List[Dict], default=None): Pricing plans
  - Each plan: `{"name": str, "price": int, "currency": str, "features": List[str], "description": str, "featured": bool}`
- `locations` (List[Dict], default=None): Contact locations
- `theme` (str, default="dark"): Theme name
- `nav_links` (list, default=["features","pricing","contact","faq"]): Navigation links

**Returns:** `Markup` - Complete landing page HTML

**Example:**
```python
from microui import LandingPage

@app.get("/")
async def landing():
    return LandingPage.render(
        title="MyApp",
        hero_title="Build Amazing Applications",
        hero_subtitle="The fastest way to create modern web apps with Python",
        cta_text="Get Started Free",
        cta_link="/signup",
        features=[
            {
                "icon": "⚡",
                "title": "Lightning Fast",
                "desc": "Optimized for speed and performance",
                "image": "https://picsum.photos/400/300?random=1"
            },
            {
                "icon": "🎨",
                "title": "Beautiful Design",
                "desc": "Stunning UI components out of the box",
                "image": "https://picsum.photos/400/300?random=2"
            },
            {
                "icon": "🔒",
                "title": "Secure by Default",
                "desc": "Built-in security best practices",
                "image": "https://picsum.photos/400/300?random=3"
            }
        ],
        pricing=[
            {
                "name": "Free",
                "price": 0,
                "currency": "$",
                "features": ["5 projects", "Email support", "1GB storage"],
                "description": "Perfect for trying out",
                "featured": False
            },
            {
                "name": "Pro",
                "price": 29,
                "currency": "$",
                "features": ["Unlimited projects", "Priority support", "100GB storage", "API access"],
                "description": "For professionals",
                "featured": True
            },
            {
                "name": "Enterprise",
                "price": 99,
                "currency": "$",
                "features": ["Everything in Pro", "24/7 support", "Unlimited storage", "SLA guarantee"],
                "description": "For large teams",
                "featured": False
            }
        ],
        theme="dark",
        nav_links=["features", "pricing", "contact"]
    )
```

---

## KanbanLayout

Kanban board layout for task management.

### KanbanLayout.render()

**Parameters:**
- `title` (str): Page title
- `columns` (List[Dict]): Kanban columns
  - Each column: `{"title": str, "tasks": List[{"title": str, "description": str, "priority": str, "priority_variant": str, "assignee_avatar": str}]}`
- `theme` (str, default="dark"): Theme name

**Returns:** `Markup` - Complete kanban board HTML (uses DashBordLayout)

**Example:**
```python
from microui import KanbanLayout

@app.get("/kanban")
async def kanban():
    return KanbanLayout.render(
        title="Project Board",
        columns=[
            {
                "title": "To Do",
                "tasks": [
                    {
                        "title": "Design Homepage",
                        "description": "Create mockups for new homepage",
                        "priority": "High",
                        "priority_variant": "error",
                        "assignee_avatar": "avatar1.jpg"
                    },
                    {
                        "title": "API Integration",
                        "description": "Integrate payment API",
                        "priority": "Medium",
                        "priority_variant": "warning"
                    }
                ]
            },
            {
                "title": "In Progress",
                "tasks": [
                    {
                        "title": "User Authentication",
                        "description": "Implement OAuth2",
                        "priority": "High",
                        "priority_variant": "error",
                        "assignee_avatar": "avatar2.jpg"
                    }
                ]
            },
            {
                "title": "Done",
                "tasks": [
                    {
                        "title": "Database Setup",
                        "description": "PostgreSQL configuration",
                        "priority": "Normal",
                        "priority_variant": "success"
                    }
                ]
            }
        ],
        theme="dark"
    )
```

---

## EcommerceLayout

E-commerce page layout with cart and product navigation.

### EcommerceLayout.render()

**Parameters:**
- `title` (str): Page title
- `content` (str): Main content HTML
- `cart_count` (int, default=0): Number of items in cart
- `brand` (str, default="🛍️ Ma Boutique"): Store brand name
- `theme` (str, default="dark"): Theme name

**Returns:** `Markup` - Complete e-commerce page HTML

**Example:**
```python
from microui import EcommerceLayout, Card, Button

@app.get("/shop")
async def shop():
    # Build product grid
    products_html = '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">'
    
    products = [
        {"name": "Product 1", "price": "$29", "image": "product1.jpg"},
        {"name": "Product 2", "price": "$49", "image": "product2.jpg"},
        {"name": "Product 3", "price": "$99", "image": "product3.jpg"}
    ]
    
    for product in products:
        products_html += Card.render(
            title=product["name"],
            body=f'<p class="text-2xl font-bold">{product["price"]}</p>',
            image=product["image"],
            actions=Button.render("Add to Cart", variant="primary")
        )
    
    products_html += '</div>'
    
    return EcommerceLayout.render(
        title="Shop",
        content=products_html,
        cart_count=3,
        brand="🛍️ My Store",
        theme="light"
    )
```

---

## Usage Tips

### Dashboard with Dynamic Content

```python
from microui import DashBordLayout
from markupsafe import Markup

@app.get("/dashboard")
async def dashboard():
    # Query database
    stats = get_dashboard_stats()
    
    content = Markup(f"""
        <div class="stats shadow mb-8">
            <div class="stat">
                <div class="stat-title">Users</div>
                <div class="stat-value">{stats['users']}</div>
            </div>
        </div>
    """)
    
    return DashBordLayout.render(
        title="Dashboard",
        content=content,
        user_name=current_user.name
    )
```

### Landing Page with Custom Sections

```python
# Add custom content to landing page
landing = LandingPage.render(
    title="MyApp",
    hero_title="Welcome",
    hero_subtitle="Get started today",
    features=[...],  # Custom features
    pricing=[...]    # Custom pricing
)
```

### Kanban with HTMX

```python
# Tasks can use HTMX for drag-and-drop
columns = [
    {
        "title": "To Do",
        "tasks": [
            {
                "title": "Task",
                "description": "Details",
                # Add hx-* attributes in task rendering
            }
        ]
    }
]
```

---

📚 **[Back to MicroUI Documentation](README.md)**
