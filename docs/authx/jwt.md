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


## 🔑 Token Management (JWT)

This module handles token generation and validation using `python-jose`.
It supports **access tokens** and **refresh tokens**, with configurable expiration through `AuthConfig`.

---

### 📌 Token Generation

Two token types are supported:

| Token Type    | Purpose                                   | Default Lifetime |
| ------------- | ----------------------------------------- | ---------------- |
| Access Token  | Authenticates API requests                | 15 minutes       |
| Refresh Token | Requests a new access token without login | 7 days           |

Token creation functions:

```python
from authx.jwt import create_access_token, create_refresh_token

access = create_access_token(user_id="123", config=config)
refresh = create_refresh_token(user_id="123", config=config)
```

---

### ⚙️ Internal Structure

All JWTs include:

| Claim  | Description                            |
| ------ | -------------------------------------- |
| `sub`  | User identifier                        |
| `exp`  | Expiration timestamp                   |
| `iat`  | Issued-at timestamp                    |
| `type` | Token category (`access` or `refresh`) |

A lower-level generic token generator is also available:

```python
create_token(data, config, token_type, expiration)
```

---

### 🔍 Token Validation

To verify and decode a token:

```python
from authx.jwt import decode_token

payload = decode_token(token, config, expected_type="access")
```

Validation enforces:

* Signature correctness
* Algorithm matching
* Token type (`access` or `refresh`)
* Expiration validity

---

### ❌ Error Handling

Token validation may raise:

| Exception               | When                                            |
| ----------------------- | ----------------------------------------------- |
| `InvalidTokenException` | Wrong format, wrong signature, wrong token type |
| `TokenExpiredException` | Token is correctly signed but expired           |

Example:

```python
try:
    payload = decode_token(token, config, "access")
except TokenExpiredException:
    return {"error": "Token expired"}
except InvalidTokenException:
    return {"error": "Invalid token"}
```

---

### 🔐 Security Notes

* Use a **long, randomly generated secret key**
* Prefer `RS256` for distributed systems and external clients
* Never log tokens in plaintext
* Rotate and invalidate refresh tokens when possible

---

### 📚 Example Workflow

```
[ User Login ]
        |
        v
 Create Access + Refresh Tokens
        |
        v
 Access Token used for API calls
        |
        └─> If expired → Refresh Token used to request a new Access Token
```

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
