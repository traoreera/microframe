# Responsive Layouts

Documentation for responsive layouts in `microui/layouts/`.

These layouts provide a starting point for building responsive user interfaces that adapt to different screen sizes.

## ResponsiveLayout

The `ResponsiveLayout` component is the primary way to create a responsive UI. It acts as a wrapper that selects the appropriate layout (either `DesktopLayout` or `MobileLayout`) based on the `device` prop.

### ResponsiveLayout.render()

**Parameters:**
- `device` (str, default="desktop"): The device type to render for. Can be "desktop" or "mobile".
- `...`: All other props are passed through to the selected layout (`DesktopLayout` or `MobileLayout`).

**Example:**
```python
from microui.layouts import ResponsiveLayout

@app.get("/")
async def home(request):
    # In a real app, you would determine the device from the request,
    # for example by inspecting the User-Agent header.
    device_type = "mobile" if "mobi" in request.headers.get("user-agent", "").lower() else "desktop"

    return ResponsiveLayout.render(
        device=device_type,
        title="My App",
        sidebar_items=[
            {"text": "Dashboard", "href": "/", "icon": "📊", "active": True},
            {"text": "Users", "href": "/users", "icon": "👥"},
        ],
        nav_items=[
            {"text": "Home", "href": "/", "icon": "🏠", "active": True},
            {"text": "Search", "href": "/search", "icon": "🔍"},
            {"text": "Profile", "href": "/profile", "icon": "👤"},
        ],
        main_content="<h1>Welcome to the app!</h1>",
        user_name="Eliezer"
    )
```

---

## DesktopLayout

A layout optimized for larger screens, featuring a persistent sidebar and a top navbar.

### DesktopLayout.render()

**Parameters:**
- `title` (str): Page title.
- `sidebar_items` (List[Dict]): A list of items for the sidebar navigation.
- `main_content` (str): The HTML content for the main area.
- `user_name` (str): The name of the currently logged-in user.
- `avatar_src` (Optional[str]): URL for the user's avatar image.
- `notifications_count` (int): Number of notifications to display.
- `brand_text` (str): The text or logo for the brand.
- `theme` (str): The DaisyUI theme to use (e.g., "light", "dark").
- `classes` (str): Additional CSS classes for the body.

**Example:**
```python
from microui.layouts import DesktopLayout

@app.get("/desktop")
async def desktop_view():
    return DesktopLayout.render(
        title="Desktop Dashboard",
        sidebar_items=[
            {"text": "Dashboard", "href": "/", "icon": "📊", "active": True},
        ],
        main_content="<p>This is the main content, viewed on a desktop.</p>",
        user_name="Eliezer"
    )
```

---

## MobileLayout

A layout designed for smaller screens, featuring a top bar and a bottom navigation menu for easy access with a thumb.

### MobileLayout.render()

**Parameters:**
- `title` (str): The title displayed in the top bar.
- `nav_items` (List[Dict]): A list of items for the bottom navigation.
- `main_content` (str): The HTML content for the main area.
- `user_name` (str): The name of the user, shown in the top bar.
- `avatar_src` (Optional[str]): URL for the user's avatar.
- `brand_text` (str): The text or logo for the brand.
- `theme` (str): The DaisyUI theme to use.
- `classes` (str): Additional CSS classes for the body.

**Example:**
```python
from microui.layouts import MobileLayout

@app.get("/mobile")
async def mobile_view():
    return MobileLayout.render(
        title="Mobile App",
        nav_items=[
            {"text": "Home", "href": "/", "icon": "🏠", "active": True},
            {"text": "Feed", "href": "/feed", "icon": "🔥"},
            {"text": "Messages", "href": "/messages", "icon": "💬"},
        ],
        main_content="<p>This is the main content, viewed on a mobile device.</p>",
        user_name="Eliezer"
    )
```

---

## EcommerceLayout

A layout for e-commerce sites, featuring a prominent shopping cart icon in the navbar.

### EcommerceLayout.render()

**Parameters:**
- `title` (str): Page title.
- `main_content` (str): The HTML content for the main area.
- `cart_item_count` (int): The number of items in the shopping cart.
- `user_name` (str): The name of the currently logged-in user.
- `avatar_src` (Optional[str]): URL for the user's avatar image.
- `brand_text` (str): The text or logo for the brand.
- `theme` (str): The DaisyUI theme to use.
- `classes` (str): Additional CSS classes for the body.

**Example:**
```python
from microui.layouts import EcommerceLayout

@app.get("/shop")
async def shop_page():
    return EcommerceLayout.render(
        title="My Awesome Shop",
        main_content="<p>Product listings go here.</p>",
        cart_item_count=3,
        user_name="Eliezer"
    )
```

---

## BlogLayout

A clean, readable layout for blogs and news websites, with a focus on typography and a simple navigation structure.

### BlogLayout.render()

**Parameters:**
- `title` (str): The title of the blog post or page.
- `main_content` (str): The HTML content for the article.
- `user_name` (str): The name of the currently logged-in user.
- `avatar_src` (Optional[str]): URL for the user's avatar image.
- `brand_text` (str): The name of the blog.
- `nav_items` (List[Dict]): A list of items for the main navigation.
- `theme` (str): The DaisyUI theme to use.
- `classes` (str): Additional CSS classes for the body.

**Example:**
```python
from microui.layouts import BlogLayout

@app.get("/blog/my-first-post")
async def blog_post():
    return BlogLayout.render(
        title="My First Blog Post",
        main_content="""
            <h2>This is the beginning of my blog.</h2>
            <p>Here I will share my thoughts on various topics.</p>
        """,
        nav_items=[
            {"text": "Home", "href": "/"},
            {"text": "About Me", "href": "/about"},
        ],
        user_name="Eliezer"
    )
```
