# Dependencies

Documentation for `microframe/dependencies/manager.py` - Dependency injection system.

## Overview

MicroFrame provides a powerful and flexible dependency injection (DI) system, inspired by FastAPI, to manage and resolve dependencies for route handlers and other functions. It supports explicit `Depends()` declarations, named dependencies, caching, and automatic resolution of nested dependencies.

## `Depends` Class

The `Depends` class is used to mark a parameter as a dependency that needs to be resolved by the `DependencyManager`.

### Basic Usage

```python
from microframe.dependencies.manager import Depends

def get_db_connection():
    # Simulate a database connection
    print("Connecting to DB...")
    return {"status": "connected", "engine": "PostgreSQL"}

@app.get("/status")
async def get_app_status(db_conn = Depends(get_db_connection)):
    """
    Retrieves the application status, injecting a database connection.
    The get_db_connection function will be called and its result passed to db_conn.
    """
    return {"app_status": "running", "database": db_conn}
```

### Parameters

-   `dependency` (Callable): The callable (function or class) that provides the dependency.
-   `use_cache` (bool, optional): If `True` (default), the result of the dependency will be cached within the request scope and reused for subsequent calls to the same dependency within that request.

## Dependency Types and Resolution

The `DependencyManager` can resolve various types of dependencies, including regular functions, class instances, and asynchronous callables.

### Function Dependencies

Standard Python functions can be used as dependencies.

```python
from microframe.exceptions.exception import UnauthorizedException

def get_current_user_id(token: str): # token would typically come from a request header
    # Simulate token verification
    if token != "SECRET_TOKEN_123":
        raise UnauthorizedException("Invalid authentication token")
    return "user_abc"

@app.get("/me")
async def get_my_profile(user_id = Depends(get_current_user_id)):
    return {"user_id": user_id, "profile_data": "..."}
```

### Class Dependencies

Classes can also be dependencies. The `DependencyManager` will instantiate them.

```python
class DatabaseService:
    def __init__(self):
        self.connected = True
        print("DatabaseService initialized.")
    
    def fetch_data(self):
        return ["item1", "item2"]

@app.get("/data")
async def get_all_data(db_service: DatabaseService = Depends(DatabaseService)):
    return {"data": db_service.fetch_data()}
```

### Async Dependencies

Dependencies can be asynchronous functions. The `DependencyManager` will `await` their execution.

```python
import asyncio

async def get_async_resource():
    await asyncio.sleep(0.1) # Simulate async operation
    return {"resource_id": "res_1", "loaded": True}

@app.get("/resource")
async def get_resource(resource = Depends(get_async_resource)):
    return {"resource": resource}
```

## Nested Dependencies

Dependencies can depend on other dependencies, forming a chain of resolution.

```python
def get_session():
    # Provides a database session
    print("Getting DB session")
    return "db_session_obj"

def get_user_repository(session = Depends(get_session)):
    # Provides a user repository, which needs a session
    print(f"Creating UserRepository with {session}")
    return {"repo_type": "UserRepository", "session": session}

@app.get("/users/{user_id}")
async def get_user_detail(user_id: int, user_repo = Depends(get_user_repository)):
    return {"user_id": user_id, "details_from_repo": user_repo}
```

## Caching

Dependencies can be cached to prevent redundant computation within a single request scope.

```python
# Assuming 'app' has a register_dependency method for named dependencies
# For Depends(), set use_cache=True in its constructor.

def expensive_computation():
    print("Performing expensive computation...")
    return 42

@app.get("/compute")
async def perform_computation(result = Depends(expensive_computation, use_cache=True)):
    return {"result": result}

# The expensive_computation will only run once per request, even if called multiple times.
```

---

## `DependencyManager` Class

The `DependencyManager` is the core component responsible for resolving dependencies. It is typically instantiated once per application and used internally by the routing system.

### Methods

#### `register(name: str, func: Callable, cache: bool = False)`

Registers a named dependency that can be injected by referring to its name in a handler's signature.

-   `name` (str): The name to register the dependency under.
-   `func` (Callable): The callable that provides the dependency.
-   `cache` (bool, optional): If `True`, the result of this named dependency will be cached.

#### `resolve(func: Callable, request: Optional[Request] = None) -> Dict[str, Any]`

Resolves all dependencies for a given function by inspecting its signature. This is the primary method used by the framework to prepare arguments for route handlers.

-   `func` (Callable): The function whose dependencies need to be resolved.
-   `request` (Optional[Request]): The current Starlette request object, which can be injected into dependencies that accept it.

#### `clear_cache()`

Clears the internal cache of all resolved dependencies. This is useful for testing or when dependencies need to be re-evaluated.

### Circular Dependency Detection

The `DependencyManager` includes a mechanism to detect and prevent infinite recursion caused by circular dependencies. If a circular dependency is detected, it will raise a `MicroFrameException`.

```python
from microframe.dependencies.manager import Depends, DependencyManager
from microframe.exceptions.exception import MicroFrameException

# Example of a circular dependency
def dep_a(b_val = Depends(lambda: dep_b())):
    return f"A({b_val})"

def dep_b(a_val = Depends(lambda: dep_a())):
    return f"B({a_val})"

async def test_circular_dependency():
    manager = DependencyManager()
    try:
        await manager.resolve(dep_a)
    except MicroFrameException as e:
        print(f"Caught expected error: {e}") # Dépendance circulaire détectée: dep_b (or dep_a)
```

---

## Common Utility Dependencies

The `microframe/dependencies/manager.py` file also provides some commonly useful dependency patterns:

### `Pagination` and `get_pagination()`

A simple pagination dependency.

```python
from microframe.dependencies.manager import Pagination, get_pagination, Depends

class Pagination:
    def __init__(self, skip: int = 0, limit: int = 100, max_limit: int = 1000):
        self.skip = max(0, skip)
        self.limit = min(limit, max_limit)
    @property
    def offset(self):
        return self.skip

def get_pagination(skip: int = 0, limit: int = 100) -> Pagination:
    return Pagination(skip=skip, limit=limit)

@app.get("/items")
async def list_items(pagination: Pagination = Depends(get_pagination)):
    return {"items": [], "skip": pagination.skip, "limit": pagination.limit}
```

### `Settings` and `get_settings()`

A basic application settings dependency. In a real application, `Settings` would load from configuration files or environment variables.

```python
from microframe.dependencies.manager import Settings, get_settings, Depends

class Settings:
    def __init__(self):
        self.app_name = "MicroFramework"
        self.debug = True
        self.secret_key = "secret"

def get_settings() -> Settings:
    return Settings()

@app.get("/app-info")
async def get_app_info(settings: Settings = Depends(get_settings)):
    return {"name": settings.app_name, "debug_mode": settings.debug}
```

---

## `inject` Decorator

The `inject` decorator provides a way to automatically inject named dependencies into a function, which is useful for services or background tasks that need dependencies outside of a request context.

```python
from microframe.dependencies.manager import inject

# Assume get_db_connection and get_settings are registered named dependencies
# or directly callable without Depends() wrapper when used with @inject.

# In a more realistic scenario, these would typically be defined as regular functions
# which might themselves depend on other things or access app.state
# For simplicity here, we'll use placeholder functions.
def get_db():
    return "Database_connection_object"

def get_app_settings():
    return {"app_name": "My Injected App"}

@inject(get_db, get_app_settings)
async def process_data(db, app_settings):
    """
    Processes data using injected database connection and app settings.
    Note: The parameter names (db, app_settings) must match the dependency function names
    after removing 'get_' prefix, or be explicitly passed if using direct injection.
    """
    print(f"Processing data with DB: {db} and settings: {app_settings['app_name']}")
    return {"status": "processed", "using_db": db, "app": app_settings['app_name']}

# To run:
# await process_data() # No need to manually pass db or app_settings
```

---

## Exception Handling

For details on custom and HTTP-specific exceptions like `MicroFrameException`, `HTTPException`, `NotFoundException`, etc., please refer to the [Exceptions Documentation](./exceptions.md).

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