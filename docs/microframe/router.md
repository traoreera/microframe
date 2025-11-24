# Router

Documentation for `microframe/routing/router.py` - Route management.

## Router Class

Organize routes into modular groups.

### Basic Usage

```python
from microframe import Router

router = Router(prefix="/api/v1", tags=["API"])

@router.get("/users")
async def list_users():
    return {"users": []}

@router.post("/users")
async def create_user(data: dict):
    return {"id": 1, **data}
```

## Router Configuration

### __init__()

```python
Router(
    prefix="/api",
    tags=["API"],
    dependencies=[],
    deprecated=False,
    include_in_schema=True
)
```

**Parameters:**
- `prefix` (str): URL prefix for all routes
- `tags` (List[str]): OpenAPI tags
- `dependencies` (List): Router-level dependencies
- `deprecated` (bool): Mark as deprecated
- `include_in_schema` (bool): Include in OpenAPI schema

## Route Methods

### router.get()
```python
@router.get("/items")
async def get_items():
    return []
```

### router.post()
```python
@router.post("/items")
async def create_item(item: Item):
    return item
```

### router.put(), router.patch(), router.delete()

Similar to GET/POST.

## Nested Routers

```python
from microframe import Router, Application

# Main router
api_router = Router(prefix="/api")

# Sub-routers
users_router = Router(prefix="/users", tags=["Users"])
posts_router = Router(prefix="/posts", tags=["Posts"])

@users_router.get("/")
async def list_users():
    return []

@posts_router.get("/")
async def list_posts():
    return []

# Include sub-routers
api_router.include_router(users_router)
api_router.include_router(posts_router)

# Include in app
app = Application()
app.include_router(api_router)

# Routes: /api/users, /api/posts
```

## Router Dependencies

```python
def verify_api_key(api_key: str):
    if api_key != "secret":
        raise UnauthorizedException()
    return api_key

router = Router(
    prefix="/api",
    dependencies=[Depends(verify_api_key)]
)

# All routes in this router require API key
@router.get("/data")
async def get_data():
    return {"data": "secret"}
```

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
