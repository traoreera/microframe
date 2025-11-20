# 🛠️ MicroFrame Technical Documentation

This document provides a deep dive into the internal architecture and components of MicroFrame. It is intended for contributors and advanced users who want to understand how the framework works under the hood.

## 🏗️ Core Architecture

### Application (`microframe.core.application`)
The `Application` class is the heart of the framework, inheriting from `starlette.applications.Starlette`. It acts as the main ASGI application entry point.

- **Initialization**:
  - Loads configuration from `AppConfig`.
  - Initializes `DependencyManager`.
  - Sets up logging and exception handlers.
  - Registers internal routes for documentation (`/docs`, `/redoc`, `/openapi.json`).

- **Route Management**:
  - Uses `_routes_info` to store metadata (`RouteInfo`) for OpenAPI generation.
  - Wraps Starlette's routing system to add dependency injection and validation layers.

### Configuration (`microframe.core.config`)
`AppConfig` is a dataclass that centralizes all application settings.
- **Defaults**: Provides sensible defaults for host, port, CORS, and rate limiting.
- **Extensibility**: Can be extended or instantiated with custom values.

## 🛣️ Routing System

### Router (`microframe.routing.Router`)
The `Router` class allows for modular route organization. It mimics the main `Application` API but is designed to be included via `app.include_router()`.

- **Route Registration**:
  - Decorators (`@get`, `@post`, etc.) create `RouteInfo` objects.
  - `RouteInfo` captures path, method, handler, tags, and response models.
- **Nesting**: Routers can include other routers, allowing for deep hierarchy (e.g., `/api/v1/users`).

### RouteInfo
A data structure that holds all metadata for a specific route. This is crucial for:
- Generating OpenAPI schemas.
- resolving dependencies at runtime.
- Validating request parameters.

## 💉 Dependency Injection

### DependencyManager (`microframe.dependencies.manager`)
The dependency injection system is inspired by FastAPI but implemented with a focus on simplicity and performance.

- **Resolution Process**:
  1. **Analysis**: Inspects the handler's signature.
  2. **Recursion**: Recursively resolves dependencies defined with `Depends()`.
  3. **Caching**: If `use_cache=True` (default), results are cached within the request scope (or app scope if configured).
  4. **Injection**: Resolved dependencies are passed as keyword arguments to the handler.

- **Features**:
  - **Async/Sync Support**: Can resolve both synchronous and asynchronous dependency functions.
  - **Circular Detection**: Prevents infinite recursion loops.

## 🛡️ Middleware

MicroFrame uses standard ASGI middleware.

### CORSMiddleware (`microframe.middleware.cors`)
Handles Cross-Origin Resource Sharing headers.
- **Preflight**: Automatically handles `OPTIONS` requests.
- **Configuration**: Supports allow origins, methods, headers, and credentials.

## ✅ Validation

### RequestParser (`microframe.validation.parser`)
Integrates **Pydantic** for data validation.
- **Body Parsing**: Automatically detects Pydantic models in route signatures and parses the JSON body.
- **Query Parameters**: Parses standard type hints (str, int, bool) from query parameters.
- **Error Handling**: Converts `pydantic.ValidationError` into 422 Unprocessable Entity responses.

## ⚠️ Error Handling

### Exception Hierarchy
- `MicroFrameException`: Base class for all framework exceptions.
- `AppException`: Base for HTTP-related exceptions.
  - `NotFoundException` (404)
  - `UnauthorizedException` (401)
  - `ForbiddenException` (403)
  - `ValidationException` (422)

### Handlers
The `Application` class registers default exception handlers to return consistent JSON error responses:
```json
{
  "error": "Error message",
  "details": "Optional details"
}
```
