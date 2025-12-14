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



## 📦 Data Models
This module defines all request and response schemas used by the authentication system.
All models are implemented with **Pydantic**, ensuring validation, type safety, and automatic OpenAPI schema generation if used in compatible frameworks.

These models act as the contract between the client and the authentication layer.

---

### 🔐 LoginRequest

Represents the payload expected when a client attempts to authenticate.

```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

| Field      | Type       | Constraints                     | Notes                                          |
| ---------- | ---------- | ------------------------------- | ---------------------------------------------- |
| `email`    | `EmailStr` | `8-50 chars`                    | Must be a valid email                          |
| `password` | `str`      | `8-50 chars`                    | Plain text input, handled securely server-side |

Example:

```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

---

### 🎫 TokenResponse

Returned after successful authentication or token refresh operations.

```python
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

| Field           | Type  | Description                              |
| --------------- | ----- | ---------------------------------------- |
| `access_token`  | `str` | JWT used for authenticated API calls     |
| `refresh_token` | `str` | Token used to request a new access token |
| `token_type`    | `str` | Always `"bearer"`                        |

Example Response:

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC...",
  "refreshToken": "eyJhbGc...",
  "tokenType": "bearer"
}
```

---

### 👤 UserResponse

Represents authenticated user data returned by the system.

```python
class UserResponse(BaseModel):
    id: str
    email: str
    data: Optional[dict]
```

| Field   | Type  | Description                   |                                                         |
| ------- | ----- | ----------------------------- | ------------------------------------------------------- |
| `id`    | `str` | Unique identifier of the user |                                                         |
| `email` | `str` | User email                    |                                                         |
| `data`  | `dict | None`                         | Additional metadata (roles, preferences, profile, etc.) |

Example:

```json
{
  "id": "42",
  "email": "user@example.com",
  "data": {
    "role": "admin",
    "lang": "en"
  }
}
```

---

### 🏷 TokenPayload (JWT Claims)

Represents decoded JWT content after validation.

```python
class TokenPayload(BaseModel):
    sub: str
    type: str
    exp: int
    iat: int
```

| Claim  | Meaning                                |
| ------ | -------------------------------------- |
| `sub`  | User ID                                |
| `type` | Token category (`access` or `refresh`) |
| `exp`  | Expiration timestamp                   |
| `iat`  | Issued-at timestamp                    |

Example output after decoding:

```json
{
  "sub": "42",
  "type": "access",
  "exp": 1730082340,
  "iat": 1730078740
}
```

---

### 📌 Notes & Best Practices

* These models enforce strict input validation.
* Sensitive values (passwords) must **never** be returned back to the client.
* Field aliases allow flexibility for UI clients using alternate naming conventions.
* Ideal for use with automatic schema generation (e.g., FastAPI, Starlite, custom ASGI docs).

---

### 🔮 Possible Extensions

* Add role/scope models
* Strong password validation policies
* Extend `UserResponse` with profile and audit metadata

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
