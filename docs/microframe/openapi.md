# OpenAPI Documentation Generation

Documentation for `microframe/docs/openapi.py` - OpenAPI 3.0 schema generation.

## Overview

The `microframe/docs/openapi.py` module provides the `OpenAPIGenerator` class, a powerful tool for automatically generating an OpenAPI 3.0 specification (`openapi.json`) for your MicroFrame application. This specification can then be used by various tools like Swagger UI or ReDoc to render interactive API documentation, making your API easier to understand and consume.

The generator leverages the `RouteInfo` objects collected from your application's registered routes, extracting details such as paths, HTTP methods, tags, summaries, descriptions, request bodies (Pydantic models), and response models.

### Purpose

-   **Automatic API Documentation**: Eliminates manual documentation efforts by generating a machine-readable API specification.
-   **Interactive UI Integration**: Provides the necessary `.json` schema for tools like Swagger UI and ReDoc to build interactive API explorers.
-   **Consistency**: Ensures that your API documentation is always in sync with your codebase.
-   **Developer Experience**: Improves the experience for API consumers by offering clear and comprehensive API details.

## `OpenAPIGenerator` Class

### Initialization

```python
class OpenAPIGenerator:
    def __init__(
        self,
        routes: List[RouteInfo],
        title: str = "API",
        version: str = "1.0.0",
        description: str = "",
        contact: Optional[Dict[str, str]] = None,
        license_info: Optional[Dict[str, str]] = None,
    ):
        # ...
```

**Parameters:**
-   `routes` (List[RouteInfo]): A list of all `RouteInfo` objects from your application's router.
-   `title` (str): The title of your API (e.g., "My Awesome API").
-   `version` (str): The version of your API (e.g., "1.0.0").
-   `description` (str): A detailed description of your API.
-   `contact` (Optional[Dict[str, str]]): Contact information for the API (e.g., `{"name": "Support", "url": "http://www.example.com/support", "email": "support@example.com"}`).
-   `license_info` (Optional[Dict[str, str]]): License information for the API (e.g., `{"name": "MIT", "url": "https://opensource.org/licenses/MIT"}`).

### Key Methods

#### `generate() -> Dict[str, Any]`

This is the main method that orchestrates the entire OpenAPI schema generation process. It returns a Python dictionary representing the complete OpenAPI 3.0 specification.

**Returns:** `Dict[str, Any]` - The generated OpenAPI 3.0 JSON schema as a Python dictionary.

#### Internal Helper Methods

The `OpenAPIGenerator` uses several internal methods to construct different parts of the OpenAPI schema:

-   `_generate_paths()`: Creates the `/paths` section, detailing each endpoint and its operations.
-   `_generate_operation(route: RouteInfo, path: str)`: Builds the details for a single HTTP operation (GET, POST, etc.), including parameters, request bodies, and responses.
-   `_generate_responses(route: RouteInfo, docstring: Dict)`: Defines the possible responses for an operation, including success and error scenarios (e.g., 200, 404, 422, 500).
-   `_parse_docstring(func: callable)`: Extracts summary, description, parameters, and return information from a handler function's docstring to enrich the documentation.
-   `_is_pydantic_model(annotation)`: Utility to check if a type annotation is a Pydantic model, indicating a request body or response schema.
-   `_get_response_schema(response_model: Any)`: Determines the OpenAPI schema for the response model, utilizing Pydantic models when available.
-   `_get_parameter_info(annotation: Any, param: inspect.Parameter)`: Extracts type, format, and example information for a given parameter.

## Integration with MicroFrame

The `OpenAPIGenerator` is typically integrated into the `Application` class of MicroFrame. When you initialize your `Application` with configuration that enables OpenAPI documentation (e.g., `openapi_url`, `docs_url`, `redoc_url`), the framework uses `OpenAPIGenerator` to create and serve the `openapi.json` endpoint.

### Example Usage (Conceptual)

You don't usually call `OpenAPIGenerator` directly; it's handled by your `Application` instance.

```python
# In your main application file (e.g., app.py)
from microframe import Application, AppConfig, Router
from pydantic import BaseModel

# Define a Pydantic model for request/response
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Configure your application
config = AppConfig(
    title="My Item API",
    version="1.0.0",
    description="A simple API for managing items.",
    docs_url="/docs",       # Enables Swagger UI
    redoc_url="/redoc",     # Enables ReDoc
    openapi_url="/openapi.json" # Exposes the OpenAPI schema
)

app = Application(configuration=config)

# Create a router
items_router = Router(prefix="/items", tags=["Items"])

@items_router.post("/", response_model=Item, status_code=201, summary="Create a new item")
async def create_item(item: Item):
    """
    Creates a new item in the system.
    Args:
        item: The item details to create.
    Returns:
        The created item with its ID.
    """
    # In a real app, this would save to a database
    return item # Return the item as it was created

@items_router.get("/{item_id}", response_model=Item, summary="Retrieve an item by ID")
async def get_item(item_id: int):
    """
    Fetches a single item by its unique identifier.
    Args:
        item_id: The ID of the item to retrieve.
    Returns:
        The requested item.
    Raises:
        NotFoundException: If the item with the given ID does not exist.
    """
    # Simulate item retrieval
    if item_id == 1:
        return Item(id=1, name="Example Item", description="This is an example.")
    raise HTTPException(status_code=404, detail="Item not found")

app.include_router(items_router)

# When you run your application, the /openapi.json endpoint will be available,
# and /docs (Swagger UI) and /redoc (ReDoc) will display the generated documentation.
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