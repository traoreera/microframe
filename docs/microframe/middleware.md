# Middleware

Documentation for middleware components in `microframe/middleware/`.

## CORS Middleware

Cross-Origin Resource Sharing middleware from `cors.py`.

### Basic Usage

```python
from microframe import Application
from microframe.middleware import CORSMiddleware

app = Application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=3600
)
```

**Parameters:**
- `allow_origins` (List[str]): Allowed origins ("*" for all)
- `allow_methods` (List[str]): Allowed HTTP methods
- `allow_headers` (List[str]): Allowed headers
- `allow_credentials` (bool): Allow credentials
- `max_age` (int): Preflight cache duration (seconds)

### Examples

**Development (Allow All):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**Production (Specific Origins):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://example.com",
        "https://api.example.com"
    ],
    allow_methods=["GET", "POST"],
    allow_credentials=True
)
```

## Security Middleware

Security headers middleware from `security_middleware.py`.

### Basic Usage

```python
from microframe.middleware import SecurityMiddleware

app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,
    rate_limit_window=60,
    enable_security_headers=True
)
```

**Parameters:**
- `rate_limit_requests` (int): Max requests per window
- `rate_limit_window` (int): Window duration (seconds)
- `enable_security_headers` (bool): Add security headers

### Security Headers

Automatically adds:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`
- `Content-Security-Policy`

### Rate Limiting

```python
app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=10,  # 10 requests
    rate_limit_window=60     # per minute
)

# Returns 429 Too Many Requests when exceeded
```

## Custom Middleware

Create custom middleware:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Before request
        print(f"Request: {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # After request
        response.headers["X-Custom-Header"] = "value"
        
        return response

app.add_middleware(CustomMiddleware)
```

---

📚 **[Back to MicroFrame Documentation](README.md)**
