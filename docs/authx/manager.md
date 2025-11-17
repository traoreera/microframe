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
| `get_user_by_email(email)`         | ✔️              | Retrieve a user record by email             |
| `get_user_by_id(id)`               | ✔️              | Retrieve a user record by unique identifier |
| `verify_password(email, password)` | ✔️              | Validate user credentials                   |
| `authenticate(email, password)`    | ❌ (implemented) | High-level login helper using the above     |

---

### 📜 Abstract Interface

```python
class AuthManager(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: Any) -> Optional[UserResponse]:
        ...

    @abstractmethod
    async def verify_password(self, email: str, password: str) -> bool:
        ...

    async def authenticate(self, email: str, password: str) -> Optional[UserResponse]:
        ...
```

---

### 💡 Behavior of `authenticate()`

The built-in `authenticate()` method performs:

1. Password validation through `verify_password()`
2. If valid → returns the associated user object via `get_user_by_email()`
3. If invalid → returns `None`

This keeps the workflow simple and predictable:

```python
user = await manager.authenticate(email, password)
if user:
    # valid login
else:
    # authentication failed
```

---

### 🧪 Example Implementation (SQLite-Style)

```python
from passlib.context import CryptContext

class SQLiteAuthManager(AuthManager):
    def __init__(self, db):
        self.db = db
        self.password_context = CryptContext(schemes=["bcrypt"])

    async def get_user_by_email(self, email: str):
        return await self.db.fetch_user(email=email)

    async def get_user_by_id(self, user_id: str):
        return await self.db.fetch_user(id=user_id)

    async def verify_password(self, email: str, password: str) -> bool:
        user = await self.get_user_by_email(email)
        if not user:
            return False
        return self.password_context.verify(password, user.password_hash)
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
