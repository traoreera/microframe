# Navigation
<nav class="nav">
  <ul>
    <li><a href="./intro.md">AuthX</a></li>
    <li><a href="./config.md">Config</a></li>
    <li><a href="./jwt.md">JWT</a></li>
    <li><a href="./manager.md">Manager</a></li>
    <li><a href="./exceptions.md">Exceptions</a></li>
    <li><a href="./dependencies.md">Dependencies</a></li>
    <li><a href="./security.md">Security</a></li>
    <li><a href="./intro.md">Intro</a></li>
    <li><a href= "./model.md"> Model</a></li>
  </ul>
</nav>


# AuthX Dependency System

Utility layer providing lightweight dependency injection and authentication helpers for Starlette-based applications.
This module integrates seamlessly with the `AuthManager`, JWT validation logic, and request-scoped context.

---

## ✨ Features

* 🔗 **Dependency Injection System** — Inspired by FastAPI, but lightweight and framework-agnostic.
* 🔐 **JWT Authentication Helper** — Fetch the authenticated user from an incoming request.
* ⚙️ **Automatic Resolution** — Detect and execute declared dependencies dynamically.
* 🧩 **Starlette Compatible** — Works natively with Starlette handlers and ASGI request context.

---

## 📦 Installation

```bash
pip install  git+https://github.com/traoreera/authx.git
```

> (or adapt if part of a monorepo/package namespace)

---

## 🚀 Quick Example

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from authx.dependencies import Depends, get_current_user, resolve_dependencies

async def protected_endpoint(request, user = Depends(get_current_user)):
    return JSONResponse({"message": f"Hello, {user.username}!"})

async def wrapper(request):
    kwargs = await resolve_dependencies(request, protected_endpoint)
    return await protected_endpoint(**kwargs)

app = Starlette(routes=[Route("/me", wrapper)])
```

---

## 🧱 Components Overview

### `Depends`

Wrapper used to declare runtime dependencies in handler signatures.

```python
async def get_token(request):
    return request.headers.get("Authorization")

async def handler(request, token = Depends(get_token)):
    return JSONResponse({"token": token})
```

---

### `get_current_user(request)`

Extracts, validates, and resolves the logged-in user from the `Authorization` bearer token.

❌ Missing token → `CredentialsException`
❌ Token valid but user deleted → `UserNotFoundException`
✔️ Token valid → Returns `UserResponse`

Underlying flow:

```
Bearer token → decode_token() → extract subject (sub) → load user → return UserResponse
```

---

### `resolve_dependencies(request, handler)`

Parses the signature of the route handler, detects `Depends()` arguments, runs them, and returns a prepared argument map.

```python
kwargs = await resolve_dependencies(request, handler)
response = await handler(**kwargs)
```

Supports:

* async dependency functions
* request-aware dependencies
* nested dependency execution

---

## 🧠 Internal Logic Diagram

```
 ┌────────────────────────────────┐
 │ Incoming Request               │
 └───────────────┬───────────────┘
                 │
        resolve_dependencies()
                 │
        ┌────────▼─────────┐
        │ Scan signature    │
        │ find Depends()    │
        └────────┬─────────┘
                 │
         Execute dependency
                 │
        ┌────────▼───────────┐
        │ get_current_user() │
        └────────┬───────────┘
                 │
         decode_token → load user
                 │
        ┌────────▼───────────┐
        │ Inject kwargs       │
        └────────┬───────────┘
                 │
           Call handler()
```

---

## ⚠️ Error Handling

| Exception               | Trigger                     | Meaning               |
| ----------------------- | --------------------------- | --------------------- |
| `CredentialsException`  | Missing or invalid JWT      | Authentication failed |
| `UserNotFoundException` | Token valid, user not found | Orphaned session      |

---

## 📝 Best Practices

✔ Wrap protected routes via middleware or wrapper
✔ Always use `HTTPS` in production
✔ Rotate tokens and secrets periodically
✔ Pair with `AuthManager` and `AuthConfig` for full security stack

---

## 📚 Roadmap

* ⏳ Caching layer for dependency resolution
* 🔧 Support sync dependencies
* 🧩 Optional permission middleware integration

---
# Navigation
<nav class="nav">
  <ul>
    <li><a href="./intro.md">AuthX</a></li>
    <li><a href="./config.md">Config</a></li>
    <li><a href="./jwt.md">JWT</a></li>
    <li><a href="./manager.md">Manager</a></li>
    <li><a href="./exceptions.md">Exceptions</a></li>
    <li><a href="./dependencies.md">Dependencies</a></li>
    <li><a href="./security.md">Security</a></li>
    <li><a href="./intro.md">Intro</a></li>
    <li><a href= "./model.md"> Model</a></li>
  </ul>
</nav>

---

## 📖 Navigation

**Documentation AuthX** :
- [Introduction](intro.md)
- [Configuration](config.md)
- [JWT Tokens](jwt.md)
- [Auth Manager](manager.md)
- [Models](model.md)
- [Exceptions](exceptions.md)
- [Dependencies](dependencies.md)
- [Security](security.md)
- [License](LICENSE.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guide Authentication](../guides/authentication.md)**
