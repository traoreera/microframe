# Exceptions

Documentation for `microframe/core/exceptions.py` - Custom exception classes.

## Base Exception

### AppException

Base exception for all MicroFrame exceptions.

```python
from microframe import AppException

raise AppException("Something went wrong", status_code=400)
```

**Parameters:**
- `message` (str): Error message
- `status_code` (int, default=500): HTTP status code
- `details` (dict, optional): Additional error details

## HTTP Exceptions

### NotFoundException (404)

```python
from microframe import NotFoundException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.get(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    return user
```

### UnauthorizedException (401)

```python
from microframe import UnauthorizedException

@app.get("/protected")
async def protected(token: str):
    if not verify_token(token):
        raise UnauthorizedException("Invalid token")
    return {"data": "secret"}
```

### ForbiddenException (403)

```python
from microframe import ForbiddenException

@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: int, user=Depends(get_current_user)):
    if not user.is_admin:
        raise ForbiddenException("Admin access required")
    # Delete user
```

### BadRequestException (400)

```python
from microframe import BadRequestException

@app.post("/users")
async def create_user(data: dict):
    if not data.get("email"):
        raise BadRequestException("Email is required")
    return create_user(data)
```

### ValidationException

Validation error exception (422).

```python
from microframe import ValidationException

raise ValidationException(
    "Validation failed",
    errors={"email": "Invalid format"}
)
```

## Usage Examples

### Exception Handler

```python
from microframe import Application, AppException
from starlette.responses import JSONResponse

app = Application()

@app.exception_handler(AppException)
async def handle_app_exception(request, exc):
    return JSONResponse(
        {"error": exc.message, "details": exc.details},
        status_code=exc.status_code
    )
```

### Try-Except Pattern

```python
from microframe import NotFoundException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        item = fetch_item(item_id)
        return item
    except KeyError:
        raise NotFoundException(f"Item {item_id} not found")
```

### Custom Exception

```python
from microframe import AppException

class RateLimitExceeded(AppException):
    def __init__(self):
        super().__init__(
            "Rate limit exceeded",
            status_code=429,
            details={"retry_after": 60}
        )

# Usage
@app.get("/api/data")
async def get_data():
    if check_rate_limit_exceeded():
        raise RateLimitExceeded()
    return {"data": [...]}
```

---

📚 **[Back to MicroFrame Documentation](README.md)**
