# Exceptions

Documentation for `microframe/exceptions/exception.py` - Custom exception classes and handling.

## Overview

MicroFrame provides a structured approach to exception handling, built upon Starlette's `HTTPException`. It introduces a hierarchy of custom exceptions to ensure consistent error responses across your application, making it easier to manage and respond to various error conditions. All exceptions are designed to provide a rich payload for API clients, including status codes, messages, and optional details.

## Base Exception Payload

### `BaseExceptionPayload`

This internal class is used to standardize the structure of error responses. It ensures that all exceptions, when serialized, return a consistent dictionary format.

```python
class BaseExceptionPayload:
    # ... (details omitted for brevity)
    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "status": self.status_code,
            "timestamp": self.timestamp,
        }
        # ... (further details)
        return payload
```

## Base Exceptions

### `MicroFrameException`

This is the base exception class for all general application-level errors that are not directly tied to an HTTP status code (though it can carry one). Use this for internal errors or domain-specific issues that might later be translated into an HTTP response.

```python
from microframe.exceptions.exception import MicroFrameException

raise MicroFrameException("Something went wrong internally", status_code=500)
```

**Parameters:**
- `message` (str): The error message.
- `status_code` (int, default=500): The HTTP status code associated with the error.
- `details` (dict, optional): Additional key-value pairs providing more context about the error.

### `HTTPException`

This class extends Starlette's `HTTPException` and serves as the base for all HTTP-specific errors in MicroFrame. It automatically integrates with the `BaseExceptionPayload` to format responses.

```python
from microframe.exceptions.exception import HTTPException

raise HTTPException(status_code=400, detail="Invalid input provided")
```

**Parameters:**
- `status_code` (int): The HTTP status code (e.g., 404, 401, 403).
- `detail` (str, optional): A brief message explaining the HTTP error.
- `errors` (List[Any], optional): A list of more specific error objects, often used for validation errors.
- `code` (str, optional): A unique error code for programmatic identification.

## Specific HTTP Exceptions

MicroFrame provides several specialized `HTTPException` subclasses for common error scenarios. These automatically set the appropriate HTTP status code and a default message/code.

### `NotFoundException` (404)

Raised when a requested resource does not exist.

```python
from microframe.exceptions.exception import NotFoundException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.get(user_id) # Assume db.get() returns None if not found
    if not user:
        raise NotFoundException(f"User with ID {user_id} not found")
    return user
```

### `UnauthorizedException` (401)

Raised when authentication credentials are missing or invalid.

```python
from microframe.exceptions.exception import UnauthorizedException

@app.get("/protected")
async def protected(token_service = Depends(get_token_service)): # Assume token_service is a dependency
    token = request.headers.get("Authorization")
    if not token or not token_service.verify(token):
        raise UnauthorizedException("Authentication required or invalid credentials")
    return {"data": "secret"}
```

### `ForbiddenException` (403)

Raised when a user is authenticated but does not have the necessary permissions to access a resource.

```python
from microframe.exceptions.exception import ForbiddenException

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: int, current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise ForbiddenException("Admin access is required to delete users")
    # Logic to delete user
```

### `BadRequestException` (400)

Raised when the server cannot process the request due to client error (e.g., malformed request syntax, invalid request message framing).

```python
from microframe.exceptions.exception import BadRequestException

@app.post("/items")
async def create_item(item_data: dict):
    if not item_data.get("name"):
        raise BadRequestException("Item name is a required field")
    # Logic to create item
```

### `ValidationException` (422)

Specifically designed for Pydantic validation errors, indicating that the request data failed schema validation.

```python
from microframe.exceptions.exception import ValidationException
from pydantic import ValidationError # Often caught by the framework automatically

def process_data(data: dict):
    try:
        validated_model = MyPydanticModel(**data)
        return validated_model
    except ValidationError as e:
        # The framework's default exception handler for ValidationErrors
        # will often convert this to a ValidationException automatically.
        raise ValidationException("Invalid data provided", errors=e.errors())

@app.post("/validate-me")
async def validate_me(payload: MyPydanticModel): # Pydantic validation happens automatically here
    return {"message": "Data is valid!", "payload": payload.dict()}
```

## Custom Exception

You can also create your own custom exceptions by inheriting from `MicroFrameException` or `HTTPException`:

```python
from microframe.exceptions.exception import MicroFrameException, HTTPException

class CustomDomainError(MicroFrameException):
    def __init__(self, message: str = "A specific domain logic error occurred"):
        super().__init__(message, status_code=418) # Custom status code

class NotEnoughTeaException(HTTPException):
    def __init__(self):
        super().__init__(418, detail="I'm a teapot, and I need more tea!", code="TEAPOT_ERROR")

@app.get("/make-tea")
async def make_tea(tea_count: int):
    if tea_count < 1:
        raise NotEnoughTeaException()
    return {"message": "Tea is brewing!"}
```

## Usage Examples

### Exception Handler

MicroFrame typically registers default exception handlers to catch these exceptions and return them in a standardized JSON format. You can also register your own.

```python
from microframe import Application
from microframe.exceptions.exception import MicroFrameException
from starlette.responses import JSONResponse

app = Application() # Assuming app is your MicroFrame Application instance

@app.exception_handler(MicroFrameException)
async def handle_microframe_exception(request, exc: MicroFrameException):
    # This handler catches all exceptions inheriting from MicroFrameException
    return JSONResponse(
        exc.to_dict(), # Uses the payload.to_dict() method
        status_code=exc.payload.status_code
    )

# Note: HTTPException (and its subclasses) are usually handled by Starlette's
# default handler or a framework-provided one, converting them to JSON.
```

### Try-Except Pattern

You can also explicitly catch exceptions in your route handlers or business logic.

```python
from microframe.exceptions.exception import NotFoundException

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    try:
        product = await get_product_from_db(product_id) # A hypothetical async DB call
        return product
    except ItemNotFoundError: # A hypothetical lower-level exception
        raise NotFoundException(f"Product {product_id} not found")
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