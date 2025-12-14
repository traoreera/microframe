# Navigation
<nav class="nav">
  <ul>
    <li><a href="../intro.md">AuthX</a></li>
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

## 🧠 Auth Manager — User Authentication Backend

The `AuthManager` is an abstract base class defining the expected contract for any authentication backend.
It decouples the authentication logic from storage, allowing implementation with:

* SQL Databases (PostgreSQL, MySQL, SQLite)
* NoSQL Databases (MongoDB, Redis)
* External Identity Providers (Keycloak, Auth0, Cognito)
* In-memory or mock backends for testing

---

### 🛠 Responsibilities

Any concrete implementation must provide:

| Method                             | Required        | Responsibility                              |
| ---------------------------------- | --------------- | ------------------------------------------- |
| `authenticate(email, password)`    | ✔️              | High-level login helper using the above     |
| `get_user_by_id(id)`               | ✔️              | Retrieve a user record by unique identifier |
| `get_user_by_email(email)`         | ✔️              | Retrieve a user record by email             |


---

### 📜 Abstract Interface

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class AuthManager(ABC):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        ...
```

---

### 🧪 Example Implementation (In-Memory)

```python
class InMemoryAuthManager(AuthManager):
    fake_db = {
        "user@example.com": {
            "id": "1",
            "email": "user@example.com",
            "password": "password",
        },
    }

    async def get_user_by_email(self, email: str):
        return self.fake_db.get(email)

    async def get_user_by_id(self, user_id: str):
        for user in self.fake_db.values():
            if user["id"] == user_id:
                return user
        return None

    async def authenticate(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if user.get("password") == password:
            return user
        return None
```

---

### 🧷 Notes & Best Practices

✔ Always store passwords **hashed with a modern algorithm** (`bcrypt`, `argon2`, `pbkdf2`).
✔ Avoid returning `None` vs `Exception` inconsistently — keep behavior predictable.
✔ For distributed systems or SSO setups, you can override `authenticate()` if authentication isn’t password-based.

---

### 🔮 Future Extensions

* User roles & scopes
* Account lockout and login throttling
* 2FA / WebAuthn
* External OAuth2 providers

---
# Navigation
<nav class="nav">
  <ul>
    <li><a href="../intro.md">AuthX</a></li>
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
