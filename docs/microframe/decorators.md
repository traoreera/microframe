# Routing Decorators

Documentation for `microframe/routing/decorators.py` - Internal route decorators.

## Overview

The `microframe/routing/decorators.py` module contains internal helper functions used to construct `RouteInfo` objects from the parameters provided to the user-facing HTTP method decorators (like `@app.get()`, `@router.post()`, etc.). Its primary role is to abstract away the direct instantiation of `RouteInfo` objects, ensuring consistency and reducing boilerplate within the routing system.

Developers typically interact with the routing decorators provided by `microframe.Application` or `microframe.Router` classes, which in turn utilize the `route_decorator` defined here.

### Purpose

-   **Abstraction**: Hides the underlying complexity of `RouteInfo` object creation from the public API.
-   **Consistency**: Ensures that all route definitions are converted into `RouteInfo` objects in a standardized manner.
-   **Internal Helper**: Serves as a foundational component for building the more elaborate routing decorators.

## `route_decorator(path: str, func: Callable, methods: List[str], **kwargs) -> RouteInfo`

This function is responsible for taking the core arguments of a route (path, handler function, HTTP methods) along with any additional keyword arguments (like `tags`, `summary`, `response_model`, etc.) and packaging them into a `RouteInfo` instance.

### Parameters

-   `path` (str): The URL path pattern for the route.
-   `func` (Callable): The asynchronous handler function for the route.
-   `methods` (List[str]): A list of HTTP methods (e.g., `["GET"]`, `["POST", "PUT"]`) that the route responds to.
-   `**kwargs`: Arbitrary keyword arguments that are directly passed to the `RouteInfo` constructor (e.g., `tags`, `summary`, `description`, `response_model`, `status_code`, `deprecated`, `include_in_schema`, `dependencies`).

### Returns

-   `RouteInfo`: An instance of the `RouteInfo` dataclass, encapsulating all the provided route metadata.

### Example Usage (Internal)

While this function is not typically called directly by end-users, here's how it's conceptually used internally by a higher-level decorator:

```python
from typing import Callable, List
from microframe.routing.models import RouteInfo
from microframe.routing.decorators import route_decorator

# Assume a handler function
async def my_example_handler():
    return {"message": "Hello from example!"}

# Internal usage to create a GET decorator
def get_decorator(path: str, **kwargs):
    def wrapper(func: Callable):
        return route_decorator(path=path, func=func, methods=["GET"], **kwargs)
    return wrapper

# How a user would then use it (via Application or Router)
# @app.get("/example") # This 'get' internally calls get_decorator
# async def some_route():
#    return await my_example_handler()

# Direct call for illustration
route_info_instance = route_decorator(
    path="/test",
    func=my_example_handler,
    methods=["GET"],
    tags=["Test"],
    summary="A test route"
)

print(route_info_instance.path)
print(route_info_instance.methods)
print(route_info_instance.summary)
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