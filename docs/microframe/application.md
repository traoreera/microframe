# Application

Documentation for `microframe/core/application.py` - The main application class.

## Application Class

The core ASGI application class that handles routing, middleware, dependencies, and exception handling.

### Initialization

```python
from microframe import Application, AppConfig

app = Application(configuration=AppConfig())
```

**Parameters:**
- `configuration` (AppConfig): Application configuration object

### Key Features

- ASGI application built on Starlette
- Route registration and management
- Dependency injection
- Middleware support
- Exception handling
- OpenAPI documentation

## Methods

### Route Registration

#### app.get()
Register a GET route.

```python
@app.get("/users")
async def get_users():
    return {"users": []}
```

**Parameters:**
- `path` (str): Route path
- `tags` (List[str], optional): OpenAPI tags
- `summary` (str, optional): Route summary
- `description` (str, optional): Route description
- `response_model` (Type, optional): Response model
- `status_code` (int): HTTP status code

#### app.post()
Register a POST route.

```python
@app.post("/users")
async def create_user(data: UserCreate):
    return {"id": 1, **data.dict()}
```

#### app.put()
Register a PUT route.

#### app.delete()
Register a DELETE route.

#### app.patch()
Register a PATCH route.

### Router Management

#### app.include_router()
Include a router in the application.

```python
from microframe import Router

users_router = Router(prefix="/users")
app.include_router(users_router)
```

**Parameters:**
- `router` (Router): Router instance
- `prefix` (str, optional): URL prefix override
- `tags` (List[str], optional): Additional tags

### Dependency Management

#### app.register_dependency()
Register a named dependency.

```python
def get_db():
    return Database()

app.register_dependency("db", get_db, cache=True)
```

**Parameters:**
- `name` (str): Dependency name
- `func` (Callable): Dependency function
- `cache` (bool): Enable caching

### Middleware

#### app.add_middleware()
Add middleware to the application.

```python
from microframe.middleware import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"]
)
```

**Parameters:**
- `middleware_class` (Type): Middleware class
- `**options`: Middleware options

### Exception Handling

#### app.add_exception_handler()
Register custom exception handler.

```python
from microframe import AppException

@app.exception_handler(AppException)
async def handle_app_exception(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=400)
```

## Properties

### app.routes
Get all registered routes.

```python
routes = app.routes
```

**Returns:** `List[Route]`

### app.router
Access the underlying Starlette router.

### app.state
Application state storage.

```python
app.state.db = Database()
```

## Complete Example

```python
from microframe import Application, AppConfig, Router, Depends
from pydantic import BaseModel

# Configuration
config = AppConfig(
    title="My API",
    version="1.0.0",
    debug=True
)

# Application
app = Application(configuration=config)

# Model
class User(BaseModel):
    name: str
    email: str

# Dependency
def get_current_user():
    return {"id": 1, "name": "John"}

# Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "User"}

@app.post("/users")
async def create_user(user: User):
    return {"id": 1, **user.dict()}

@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user

# Router
api_router = Router(prefix="/api/v1", tags=["API"])

@api_router.get("/status")
async def status():
    return {"status": "ok"}

app.include_router(api_router)

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Lifecycle Hooks

### Startup Events

```python
@app.on_event("startup")
async def startup_event():
    # Initialize database, cache, etc.
    app.state.db = await create_db_connection()
```

### Shutdown Events

```python
@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    await app.state.db.close()
```

## Internal Methods

### _register_route()
Internal route registration.

### _resolve_dependencies()
Resolve route dependencies.

### _app_exception_handler()
Handle AppException.

### _validation_exception_handler()
Handle validation errors.

### _generic_exception_handler()
Catch-all exception handler.

---

## 📖 Navigation

**Documentation Modules Core** :
- [Index Modules](README.md)
- [Application](application.md)
- [Config](config.md)
- [Router](router.md)
- [Dependencies](dependencies.md)
- [Validation](validation.md)
- [Middleware](middleware.md)
- [Exceptions](exceptions.md)
- [Templates](templates.md)
- [UI Components](ui.md)
- [Configurations](configurations.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guides Pratiques](../guides/getting-started.md)**
