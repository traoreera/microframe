# Route Registry

Documentation for `microframe/routing/registry.py` - Route registry for tracking all routes.

## RouteRegistry Class

The `RouteRegistry` class serves as a centralized manager for all `RouteInfo` objects within the MicroFrame application. It provides mechanisms to register routes and retrieve them efficiently based on their path or associated tags. This registry is crucial for the application's routing system, allowing the application to quickly find and process route definitions.

### Purpose

-   **Centralized Storage**: Maintains a single, consistent collection of all defined routes.
-   **Efficient Retrieval**: Allows for quick lookup of routes by their URL path or by the tags assigned to them.
-   **OpenAPI Integration**: Facilitates the collection of route information needed for OpenAPI documentation generation.
-   **Dynamic Routing**: Supports applications that might dynamically add or remove routes during their lifecycle.

### Methods

#### `__init__()`

Initializes an empty `RouteRegistry`. It sets up internal lists and dictionaries to store `RouteInfo` objects.

```python
class RouteRegistry:
    def __init__(self):
        self._routes: List[RouteInfo] = []
        self._by_path: Dict[str, List[RouteInfo]] = {}
        self._by_tag: Dict[str, List[RouteInfo]] = {}
```

#### `register(route_info: RouteInfo)`

Registers a single `RouteInfo` object with the registry. It adds the route to the main list and indexes it by its path and all its associated tags for faster lookup.

**Parameters:**
-   `route_info` (RouteInfo): An instance of the `RouteInfo` dataclass containing all details about the route.

#### `get_all() -> List[RouteInfo]`

Returns a copy of all `RouteInfo` objects currently registered in the system.

**Returns:** `List[RouteInfo]` - A list of all registered route information objects.

#### `get_by_path(path: str) -> List[RouteInfo]`

Retrieves a list of `RouteInfo` objects that match the given URL path.

**Parameters:**
-   `path` (str): The URL path to search for.

**Returns:** `List[RouteInfo]` - A list of `RouteInfo` objects matching the path, or an empty list if no routes are found.

#### `get_by_tag(tag: str) -> List[RouteInfo]`

Retrieves a list of `RouteInfo` objects that are associated with the specified tag.

**Parameters:**
-   `tag` (str): The tag to search for.

**Returns:** `List[RouteInfo]` - A list of `RouteInfo` objects associated with the tag, or an empty list if no routes are found.

#### `clear()`

Removes all registered routes and clears the internal indexes, effectively resetting the registry.

### Example Usage

```python
from microframe.routing.models import RouteInfo
from microframe.routing.registry import RouteRegistry

# Assume a dummy handler function
async def my_handler():
    pass

# Create a registry instance
registry = RouteRegistry()

# Define some RouteInfo objects
route1 = RouteInfo(path="/users", func=my_handler, methods=["GET"], tags=["Users"])
route2 = RouteInfo(path="/users/{id}", func=my_handler, methods=["GET", "PUT"], tags=["Users", "Admin"])
route3 = RouteInfo(path="/posts", func=my_handler, methods=["GET"], tags=["Posts"])

# Register the routes
registry.register(route1)
registry.register(route2)
registry.register(route3)

# Get all routes
all_routes = registry.get_all()
print(f"Total routes: {len(all_routes)}")

# Get routes by path
users_routes = registry.get_by_path("/users")
print(f"Routes for /users: {len(users_routes)}")

# Get routes by tag
admin_routes = registry.get_by_tag("Admin")
print(f"Routes with 'Admin' tag: {len(admin_routes)}")

# Clear the registry
registry.clear()
print(f"Routes after clear: {len(registry.get_all())}")
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