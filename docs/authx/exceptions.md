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
  </ul>
</nav>
---

# 🔐 AuthX — Core Authentication Module

This module provides a minimal yet reliable authentication core designed for ASGI frameworks such as **Starlette**, lightweight **FastAPI-style frameworks**, or custom micro-frameworks.

It includes dependency injection utilities, JWT authentication, current-user retrieval, and a centralized exception system.

---

## 🚀 Features

* 🧩 Pluggable dependency injection system (FastAPI-like)
* 🔑 Extract user identity from Bearer tokens
* 🛂 Configurable JWT decoding
* ⚠️ Unified authentication exception system
* 🔄 Recursive dependency resolution (`Depends`)
* 🧱 Works with `AuthConfig`, `AuthManager`, and `UserResponse`

---

## 📦 Installation

```bash
pip install authx
```

> If you're integrating it in a custom framework, adjust imports according to your project layout.

---

## 🧩 Components Overview

| Component                | Purpose                                                          |
| ------------------------ | ---------------------------------------------------------------- |
| `Depends`                | Wrapper used to mark injected dependencies                       |
| `get_current_user()`     | Extracts and verifies the authenticated user from JWT            |
| `resolve_dependencies()` | Inspects handler signatures and dynamically injects dependencies |
| Custom Exceptions        | Standardized and predictable error handling                      |

---

## ⚠️ Authentication Exceptions

| Exception               | HTTP Code | Description                       |
| ----------------------- | --------- | --------------------------------- |
| `AuthException`         | 401       | Base exception class              |
| `CredentialsException`  | 401       | Invalid or missing credentials    |
| `InvalidTokenException` | 401       | Token format or signature invalid |
| `TokenExpiredException` | 401       | Token expired                     |
| `UserNotFoundException` | 404       | User does not exist in database   |

---

## 🔧 Usage Example

```python
from authx.dependencies import Depends, get_current_user

async def protected_endpoint(
    request,
    user = Depends(get_current_user)
):
    return {"message": f"Hello {user.email}"}
```

Routing layer example using manual dependency resolution:

```python
from authx.resolver import resolve_dependencies

async def dispatch(request, handler):
    resolved_args = await resolve_dependencies(request, handler)
    return await handler(**resolved_args)
```

---

## 🪪 Expected Authorization Header

```http
Authorization: Bearer <jwt_token_here>
```

---

## 🧬 Execution Flow

1. A request hits the protected endpoint.
2. `resolve_dependencies()` inspects the function signature.
3. Any parameter wrapped with `Depends()` triggers execution of its linked function.
4. `get_current_user()` extracts and validates the JWT.
5. The function receives the authenticated `UserResponse`.

---

## 📌 Requirements

To function properly, the application must expose the following:

```python
request.app.state.auth_config   # instance of AuthConfig
request.app.state.auth_manager  # instance of AuthManager
```

---

## 🛠 Roadmap

* User lookup caching
* Multi-scope OAuth2 support
* Structured logging
* Synchronous resolution support

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
