# Routing Models

Documentation for `microframe/routing/models.py` - Routing models and data structures.

## RouteInfo Class

The `RouteInfo` dataclass is a central component for storing comprehensive metadata about each registered route within the MicroFrame application. This information is vital for various framework functionalities, including OpenAPI schema generation, accurate dependency resolution, and precise request parameter validation.

### Purpose

-   **OpenAPI Generation**: Provides all necessary details to generate accurate and rich OpenAPI documentation.
-   **Dependency Resolution**: Helps the dependency injection system understand what dependencies a route handler requires.
-   **Request Validation**: Stores information relevant for validating incoming request parameters and body.
-   **Modularity**: Encapsulates all route-specific configurations in a single, accessible structure.

### Attributes

-   `path` (str): The URL path pattern (e.g., `"/users/{user_id}"`).
-   `func` (Callable): The actual handler function that will be executed for the route.
-   `methods` (List[str]): A list of HTTP methods that the route responds to (e.g., `["GET", "POST"]`).
-   `tags` (List[str]): OpenAPI tags for grouping routes in the documentation.
-   `summary` (Optional[str]): A short summary description of the route, often used in OpenAPI UIs.
-   `description` (Optional[str]): A longer, more detailed description of the route's functionality.
-   `response_model` (Optional[Any]): A Pydantic model or other type hint representing the expected structure of the response.
-   `status_code` (int): The default HTTP status code returned on a successful response.
-   `deprecated` (bool): A flag indicating if the route is deprecated (used for OpenAPI annotations).
-   `include_in_schema` (bool): Determines whether the route should be included in the generated OpenAPI schema.
-   `dependencies` (List[Any]): A list of dependencies (often `Depends` objects) specific to this route.

### Example Definition

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RouteInfo:
    path: str
    func: Callable
    methods: List[str]
    tags: List[str] = field(default_factory=list)
    summary: Optional[str] = None
    description: Optional[str] = None
    response_model: Optional[Any] = None
    status_code: int = 200
    deprecated: bool = False
    include_in_schema: bool = True
    dependencies: List[Any] = field(default_factory=list)
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