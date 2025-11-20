# Authentication & User Pages

Documentation for authentication and user management pages from `microui/pages/`.

## AuthPages

Pre-built authentication pages (login, register, forgot password).

### AuthPages.login_page()

Complete login page with form.

**Parameters:**
- `config` (LoginConfig, default=None): Login page configuration

**LoginConfig Fields:**
- `form_action` (str): Form submission URL
- `title` (str): Page title
- `subtitle` (str): Page subtitle
- `logo` (str): Logo/icon
- `show_register_link` (bool): Show register link
- `show_forgot_password` (bool): Show forgot password link
- `register_url` (str): Register page URL
- `forgot_password_url` (str): Forgot password URL

**Returns:** `Markup` - Complete login page HTML

**Example:**
```python
from microui import AuthPages, LoginConfig

@app.get("/login")
async def login():
    config = LoginConfig(
        form_action="/auth/login",
        title="Welcome Back",
        subtitle="Sign in to your account",
        logo="🔐",
        show_register_link=True,
        show_forgot_password=True,
        register_url="/register",
        forgot_password_url="/forgot-password"
    )
    return AuthPages.login_page(config)

# Or use defaults
@app.get("/login")
async def login():
    return AuthPages.login_page()
```

### AuthPages.register_page()

Complete registration page with form.

**Parameters:**
- `config` (RegisterConfig, default=None): Register page configuration

**RegisterConfig Fields:**
- `form_action` (str): Form submission URL
- `title` (str): Page title
- `subtitle` (str): Page subtitle
- `logo` (str): Logo/icon
- `show_login_link` (bool): Show login link
- `login_url` (str): Login page URL
- `require_terms` (bool): Require terms acceptance

**Returns:** `Markup` - Complete registration page HTML

**Example:**
```python
from microui import AuthPages, RegisterConfig

@app.get("/register")
async def register():
    config = RegisterConfig(
        form_action="/auth/register",
        title="Create Account",
        subtitle="Join us today",
        logo="✨",
        show_login_link=True,
        login_url="/login",
        require_terms=True
    )
    return AuthPages.register_page(config)
```

### AuthPages.forgot_password_page()

Forgot password page.

**Parameters:**
- `form_action` (str, default="/auth/forgot-password"): Form submission URL

**Returns:** `Markup` - Complete forgot password page HTML

**Example:**
```python
from microui import AuthPages

@app.get("/forgot-password")
async def forgot_password():
    return AuthPages.forgot_password_page(
        form_action="/auth/reset-password"
    )
```

---

## ProfilePages

User profile pages.

### ProfilePages.profile_view()

View user profile page.

**Parameters:**
- `config` (ProfileConfig, default=None): Profile page configuration

**ProfileConfig Fields:**
- `user_name` (str): User name
- `user_email` (str): User email
- `user_avatar` (str): Avatar URL
- `user_bio` (str): User biography
- `edit_url` (str): Edit profile URL

**Returns:** `Markup` - Profile view page HTML

**Example:**
```python
from microui import ProfilePages, ProfileConfig

@app.get("/profile")
async def profile(request):
    user = get_current_user(request)
    
    config = ProfileConfig(
        user_name=user.name,
        user_email=user.email,
        user_avatar=user.avatar_url,
        user_bio=user.bio,
        edit_url="/profile/edit"
    )
    
    return ProfilePages.profile_view(config)
```

### ProfilePages.profile_edit()

Edit profile page with form.

**Parameters:**
- `config` (ProfileConfig): Profile configuration
- `form_action` (str): Form submission URL

**Returns:** `Markup` - Profile edit page HTML

**Example:**
```python
@app.get("/profile/edit")
async def edit_profile():
    user = get_current_user()
    
    return ProfilePages.profile_edit(
        config=ProfileConfig(...),
        form_action="/api/profile/update"
    )
```

---

## UsersManagement

User management pages for administrators.

### UsersManagement.users_list()

List all users page.

**Parameters:**
- `config` (UsersManagementConfig): Users management configuration

**UsersManagementConfig Fields:**
- `users` (List[Dict]): List of users
- `total_users` (int): Total user count
- `current_page` (int): Current page number
- `per_page` (int): Users per page

**Returns:** `Markup` - Users list page HTML

**Example:**
```python
from microui import UsersManagement, UsersManagementConfig

@app.get("/admin/users")
async def users_list():
    users = get_all_users()
    
    config = UsersManagementConfig(
        users=[
            {
                "id": "1",
                "name": "Alice",
                "email": "alice@example.com",
                "role": "Admin",
                "status": "Active"
            },
            {
                "id": "2",
                "name": "Bob",
                "email": "bob@example.com",
                "role": "User",
                "status": "Active"
            }
        ],
        total_users=50,
        current_page=1,
        per_page=20
    )
    
    return UsersManagement.users_list(config)
```

### UsersManagement.user_details()

Individual user details page.

**Parameters:**
- `user_id` (str): User ID
- `user_data` (Dict): User information

**Returns:** `Markup` - User details page HTML

**Example:**
```python
@app.get("/admin/users/{user_id}")
async def user_details(user_id: str):
    user = get_user_by_id(user_id)
    
    return UsersManagement.user_details(
        user_id=user_id,
        user_data={
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
            "last_login": user.last_login
        }
    )
```

---

## SettingsPages

Application and user settings pages.

### SettingsPages.general_settings()

General settings page.

**Parameters:**
- `config` (SettingsConfig): Settings configuration

**SettingsConfig Fields:**
- `app_name` (str): Application name
- `app_description` (str): Description
- `settings` (Dict): Current settings

**Returns:** `Markup` - Settings page HTML

**Example:**
```python
from microui import SettingsPages, SettingsConfig

@app.get("/settings")
async def settings():
    config = SettingsConfig(
        app_name="MyApp",
        app_description="My Application",
        settings={
            "notifications_enabled": True,
            "dark_mode": True,
            "language": "en"
        }
    )
    
    return SettingsPages.general_settings(config)
```

### SettingsPages.security_settings()

Security settings page.

**Returns:** `Markup` - Security settings page HTML

**Example:**
```python
@app.get("/settings/security")
async def security_settings():
    return SettingsPages.security_settings()
```

---

## AuthComponents

Reusable authentication UI components.

### AuthComponents.login_form()

Standalone login form component.

**Parameters:**
- `action` (str): Form action URL
- `show_remember` (bool): Show remember me checkbox

**Returns:** `Markup` - Login form HTML

**Example:**
```python
from microui import AuthComponents

# Use in custom page
login_form = AuthComponents.login_form(
    action="/auth/login",
    show_remember=True
)
```

### AuthComponents.register_form()

Standalone registration form component.

**Parameters:**
- `action` (str): Form action URL
- `require_terms` (bool): Require terms acceptance

**Returns:** `Markup` - Registration form HTML

---

## Complete Authentication Flow Example

```python
from microframe import Application
from microui import AuthPages, LoginConfig, RegisterConfig

app = Application()

@app.get("/login")
async def login():
    return AuthPages.login_page(
        LoginConfig(
            form_action="/auth/login",
            title="Welcome",
            show_register_link=True
        )
    )

@app.post("/auth/login")
async def handle_login(request):
    form = await request.form()
    # Validate credentials
    if authenticate(form["email"], form["password"]):
        # Set session
        return RedirectResponse("/dashboard")
    else:
        # Show error with config
        return AuthPages.login_page(
            LoginConfig(error="Invalid credentials")
        )

@app.get("/register")
async def register():
    return AuthPages.register_page(
        RegisterConfig(
            form_action="/auth/register",
            require_terms=True
        )
    )

@app.post("/auth/register")
async def handle_register(request):
    form = await request.form()
    # Create user
    user = create_user(form)
    return RedirectResponse("/login")
```

---

📚 **[Back to MicroUI Documentation](README.md)**
