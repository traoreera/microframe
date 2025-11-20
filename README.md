# 🚀 MicroFrame v2.0 - Modular Architecture

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MicroFramework v2.0** is a modern ASGI micro-framework with an optimized modular architecture, inspired by FastAPI.

## ✨ What's New in v2.0

- 🎯 **Modular Architecture** - Code organized into independent modules
- ⚡ **Optimized Performance** - Intelligent caching and fast resolution
- 🎨 **MicroUI Library** - 50+ DaisyUI components with lazy loading (~60% faster)
- 🔧 **Centralized Configuration** - `AppConfig` for all settings
- 🧪 **Improved Testability** - Independent modules are easy to test
- 📚 **Comprehensive Documentation** - Detailed guides and examples
- 🔒 **Typed Exceptions** - `NotFoundException`, `UnauthorizedException`, etc.
- 🏗️ **Page Layouts** - Ready-to-use dashboard, landing, kanban templates


## 📦 Quick Installation

```bash
git clone https://github.com/traoreera/microframe.git
cd microframework
pip install -e . 
#or
poetry init 
poetry add git+https://github.com/traoreera/microframe.git
#or
python -m venv .env
source .env/bin/activate
pip install git+https://github.com/traoreera/microframe.git
```

## 🚀 Quick Start

### Simple Application

```python
from microframe import Application

app = Application(
    title="My API",
    version="1.0.0",
    description="A simple API"
)

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id, "name": "John"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### With Modular Routers

```python
from microframe import Application, Router
from pydantic import BaseModel

# Define a model
class User(BaseModel):
    name: str
    email: str
    age: int

# Create a router
users_router = Router(prefix="/users", tags=["Users"])

@users_router.get("/")
async def list_users():
    return {"users": [{"id": 1, "name": "Alice"}]}

@users_router.post("/")
async def create_user(user: User):
    return {"message": "User created", "user": user}

# Application
app = Application(title="Modular API")
app.include_router(users_router)
```

### With Dependency Injection

```python
from microframe import Application, Depends

def get_database():
    return {"type": "postgres", "connected": True}

@app.get("/data")
async def get_data(db=Depends(get_database)):
    return {"data": "...", "database": db}
```

### With Middleware

```python
from microframe import Application
from microframe.middleware import CORSMiddleware, SecurityMiddleware

app = Application()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)

# Security & Rate Limiting
app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,
    rate_limit_window=60
)
```

## 📁 Architecture

```
microframe/
├── core/               # Core module
│   ├── application.py  # Main application
│   ├── config.py       # Configuration
│   └── exceptions.py   # Exceptions
│
├── http/               # HTTP handling
│   └── handlers.py     # Handlers
│
├── routing/            # Routing system
│   ├── router.py       # Main router
│   ├── models.py       # Models
│   └── registry.py     # Registry
│
├── dependencies/       # Dependency injection
│   ├── manager.py      # Manager
│   └── models.py       # Depends
│
├── validation/         # Validation
│   └── parser.py       # Request parser
│
├── middleware/         # Middlewares
│   ├── cors.py         # CORS
│   └── security_middleware.py  # Security
│
└── docs/               # Documentation
    ├── openapi.py      # OpenAPI generator
    └── ui.py           # Swagger/ReDoc UI
```

## 🎨 MicroUI - UI Component Library

MicroFrame includes **MicroUI**, a comprehensive DaisyUI component library for Python/HTMX applications.

### Features
- 🎨 **50+ DaisyUI Components** - Buttons, cards, modals, forms, and more
- 🚀 **Lazy Loading** - ~60% faster startup with on-demand component loading
- 📱 **Fully Responsive** - Mobile-first, responsive designs
- 🎭 **30+ Themes** - Built-in DaisyUI theme support
- 🔧 **HTMX Ready** - Seamless HTMX integration
- 📦 **Zero JavaScript** - Pure Python, server-rendered
- 🏗️ **Page Layouts** - Dashboard, landing page, kanban, e-commerce

### Quick Example

```python
from microframe import Application
from microui import Button, Card, Alert, LandingPage

app = Application()

@app.get("/")
async def home():
    return LandingPage.render(
        title="My App",
        hero_title="Build Amazing Apps",
        hero_subtitle="With Python and MicroUI",
        features=[
            {"icon": "⚡", "title": "Fast", "desc": "Lightning fast"},
            {"icon": "🎨", "title": "Beautiful", "desc": "Stunning UI"},
        ]
    )

@app.get("/api")
async def api():
    return f"""
    {Alert.render("Operation successful!", type="success")}
    {Card.render(
        title="User Profile",
        body="User information here...",
        actions=Button.render("Edit", variant="primary", hx_get="/edit")
    )}
    """
```

### Available Components

**Basic**: Button, Card, Alert, Modal, Input, Table, Badge, Navbar, Loading

**Advanced**: Sidebar, Drawer, Tabs, Dropdown, Avatar, Progress, Stats, Timeline, Toast, Pagination

**Layouts**: Pricing, Contact forms

**Pages**: DashBordLayout, LandingPage, KanbanLayout, EcommerceLayout

**Auth**: AuthPages (login/register), ProfilePages, UsersManagement, SettingsPages

📚 **[Full MicroUI Documentation](microui/README.md)**

## 🎓 Examples

Check `examples/basic_app.py` for a complete example with:
- Modular routes with routers
- Pydantic validation
- Dependency injection
- Middlewares (CORS, Security)
- Nested routes


## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete architecture guide
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migration from v1.0
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Summary of changes

## 🌟 Features

### ✅ Automatic Validation with Pydantic
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    title: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)

@app.post("/items")
async def create_item(item: Item):
    return {"item": item}
```

### ✅ Auto-generated Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### ✅ Typed Error Handling
```python
from microframe import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.get(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    return user
```

### ✅ Centralized Configuration
```python
from microframe.core import AppConfig

config = AppConfig(
    title="My API",
    version="2.0.0",
    debug=True,
    cors_origins=["http://localhost:3000"],
    rate_limit_requests=100,
    rate_limit_window=60,
    max_request_size=10_000_000
)

app = Application(config=config)
```

## 🧪 Tests

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=microframe --cov-report=html
```

## 🔒 Security

- ✅ **Rate Limiting** - Protection against abuse
- ✅ **CORS** - Flexible configuration
- ✅ **Security Headers** - X-Frame-Options, CSP, HSTS
- ✅ **Payload Validation** - Size limitation
- ✅ **Method Validation** - Allowed HTTP methods

## 📊 Performance

### Framework Core
- ⚡ **Smart Cache** for dependencies
- ⚡ **Indexed Registry** for routes (O(1))
- ⚡ **Lazy Imports** for fast startup
- ⚡ **Optimized Resolution** of dependencies

### MicroUI Optimizations (v2.0)
- ⚡ **60% faster startup** - Lazy component loading
- ⚡ **80+ lines reduced** - Utility helpers eliminate duplication
- ⚡ **39% file size reduction** - Better organized code (layout.py split)
- ⚡ **Efficient rendering** - Optimized HTML generation

## 🛠️ Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run application
python examples/basic_app.py

# Code formatting
black microframe/

# Code verification
flake8 microframe/
mypy microframe/
```

## 🤝 Contribution

Contributions are welcome!

1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgements

- Inspired by [FastAPI](https://fastapi.tiangolo.com/)
- Built with [Starlette](https://www.starlette.io/)
- Validation with [Pydantic](https://pydantic-docs.helpmanual.io/)

## 📞 Contact

- GitHub: [@traoreera](https://github.com/traoreera)
- Documentation: [microframe.dev](https://microframe.dev)

---

⭐ **Don't forget to star if this project helps you!**
