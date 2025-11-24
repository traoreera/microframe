# Validation

Documentation for `microframe/validation/parser.py` - Request parsing and validation.

## Request Parsing

Automatic request body parsing with Pydantic validation.

### Basic Usage

```python
from pydantic import BaseModel
from microframe import Application

app = Application()

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
async def create_user(user: User):
    # user is automatically validated
    return {"id": 1, **user.dict()}
```

## Validation Features

### Required Fields

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    description: str = Field(default="")
```

### Field Validation

```python
from pydantic import validator

class User(BaseModel):
    email: str
    age: int
    
    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v
    
    @validator("age")
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("Must be 18+")
        return v
```

### Optional Fields

```python
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
```

## Error Handling

Validation errors return 422 Unprocessable Entity:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
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
