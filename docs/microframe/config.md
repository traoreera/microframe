# Configuration

Documentation for `microframe/core/config.py` - Application configuration.

## AppConfig Class

Dataclass for centralizing all application settings.

### Basic Configuration

```python
from microframe.core import AppConfig

config = AppConfig(
    title="My API",
    version="1.0.0",
    description="API Description",
    debug=True
)
```

## Configuration Fields

### Application Info

#### title
Application title (shown in OpenAPI docs).

**Type:** `str`  
**Default:** `"MicroFramework"`

#### version
Application version.

**Type:** `str`  
**Default:** `"2.0.0"`

#### description
Application description.

**Type:** `str`  
**Default:** `""`

#### debug
Debug mode (enables detailed error messages).

**Type:** `bool`  
**Default:** `False`

### OpenAPI Configuration

#### openapi_url
OpenAPI schema JSON endpoint.

**Type:** `Optional[str]`  
**Default:** `"/openapi.json"`  
**Note:** Set to `None` to disable

#### docs_url
Swagger UI endpoint.

**Type:** `Optional[str]`  
**Default:** `"/docs"`  
**Note:** Set to `None` to disable

#### redoc_url
ReDoc UI endpoint.

**Type:** `Optional[str]`  
**Default:** `"/redoc"`  
**Note:** Set to `None` to disable

### Server Configuration

#### host
Server host address.

**Type:** `str`  
**Default:** `"0.0.0.0"`

#### port
Server port number.

**Type:** `int`  
**Default:** `8000`

### Security Configuration

#### allowed_hosts
List of allowed host headers.

**Type:** `List[str]`  
**Default:** `["*"]`

#### secret_key
Secret key for cryptographic operations.

**Type:** `Optional[str]`  
**Default:** `None`

#### enable_security_headers
Enable security headers middleware.

**Type:** `bool`  
**Default:** `True`

### CORS Configuration

#### cors_origins
Allowed CORS origins.

**Type:** `List[str]`  
**Default:** `["*"]`

#### cors_methods
Allowed HTTP methods for CORS.

**Type:** `List[str]`  
**Default:** `["GET", "POST", "PUT", "DELETE", "OPTIONS"]`

#### cors_headers
Allowed headers for CORS.

**Type:** `List[str]`  
**Default:** `["*"]`

#### cors_credentials
Allow credentials in CORS requests.

**Type:** `bool`  
**Default:** `False`

### Rate Limiting

#### rate_limit_enabled
Enable rate limiting.

**Type:** `bool`  
**Default:** `False`

#### rate_limit_requests
Maximum requests per window.

**Type:** `int`  
**Default:** `100`

#### rate_limit_window
Time window in seconds.

**Type:** `int`  
**Default:** `60`

### Payload Limits

#### max_request_size
Maximum request size in bytes.

**Type:** `int`  
**Default:** `10_000_000` (10MB)

### Middleware

#### middleware
List of custom middleware.

**Type:** `List[Middleware]`  
**Default:** `None`

## Usage Examples

### Production Configuration

```python
from microframe.core import AppConfig

config = AppConfig(
    title="Production API",
    version="1.0.0",
    debug=False,
    host="0.0.0.0",
    port=8000,
    cors_origins=["https://example.com"],
    cors_credentials=True,
    enable_security_headers=True,
    rate_limit_enabled=True,
    rate_limit_requests=100,
    rate_limit_window=60,
    max_request_size=5_000_000
)
```

### Development Configuration

```python
config = AppConfig(
    title="Dev API",
    version="0.1.0",
    debug=True,
    cors_origins=["*"],
    rate_limit_enabled=False
)
```

### Disable Documentation

```python
config = AppConfig(
    title="Private API",
    openapi_url=None,  # Disable OpenAPI
    docs_url=None,     # Disable Swagger
    redoc_url=None     # Disable ReDoc
)
```

### Custom Middleware

```python
from microframe.middleware import CORSMiddleware, SecurityMiddleware

config = AppConfig(
    middleware=[
        (CORSMiddleware, {
            "allow_origins": ["https://example.com"],
            "allow_methods": ["GET", "POST"]
        }),
        (SecurityMiddleware, {
            "enable_xss_filter": True
        })
    ]
)
```

## Environment Variables

Load configuration from environment:

```python
import os
from microframe.core import AppConfig

config = AppConfig(
    title=os.getenv("APP_TITLE", "My API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    debug=os.getenv("DEBUG", "false").lower() == "true",
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8000")),
    secret_key=os.getenv("SECRET_KEY"),
    cors_origins=os.getenv("CORS_ORIGINS", "*").split(",")
)
```

## Configuration File

Load from YAML/JSON:

```python
import yaml
from microframe.core import AppConfig

with open("config.yaml") as f:
    settings = yaml.safe_load(f)

config = AppConfig(**settings)
```

**config.yaml:**
```yaml
title: My API
version: 1.0.0
debug: false
host: 0.0.0.0
port: 8000
cors_origins:
  - https://example.com
rate_limit_enabled: true
rate_limit_requests: 100
```

## Best Practices

1. **Use environment variables** in production
2. **Disable debug mode** in production
3. **Set specific CORS origins** (not "*")
4. **Enable rate limiting** for public APIs
5. **Set max_request_size** to prevent DoS
6. **Use secret_key** for sessions/JWT
7. **Hide documentation** in production if needed

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
