# Navigation
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


# **AuthConfig — Authentication Configuration**

## **Overview**

`AuthConfig` centralizes all authentication-related settings used by the framework.
It defines how JWTs are generated, signed, validated, and how refresh tokens are stored and transmitted.

This configuration is required when initializing the authentication system and acts as a single source of truth for token lifecycle and security policies.

---

## **Purpose**

* Define JWT signing and verification parameters.
* Control access/refresh token expiration strategies.
* Configure secure cookie behavior for refresh tokens.
* Provide a consistent configuration interface across environments (local, staging, production).

---

## **Key Features**

* Centralized authentication settings
* Secure defaults aligned with best practices
* Support for symmetric (HS256) and asymmetric (RS256) signing
* Built-in HTTP-only and secure cookie handling
* Direct use with Starlette dependencies or DI systems

---

## **Initialization Example**

```python
from authx.config import AuthConfig

auth_config = AuthConfig(
    secret_key="your-very-long-secure-secret",
    algorithm="HS256",
    access_token_expire_minutes=30,
    refresh_token_expire_days=14,
)
```

---

## **Parameters**

| Name                          | Type                               | Default           | Description                                                                |
| ----------------------------- | ---------------------------------- | ----------------- | -------------------------------------------------------------------------- |
| `secret_key`                  | `str`                              | **Required**      | Secret used for JWT signing. Must be long and secure.                      |
| `algorithm`                   | `Literal["HS256", "RS256"]`        | `"HS256"`         | Defines signing mode. `"HS256"` → shared secret, `"RS256"` → RSA key pair. |
| `access_token_expire_minutes` | `int`                              | `15`              | Lifetime of access tokens. Should remain short.                            |
| `refresh_token_expire_days`   | `int`                              | `7`               | Lifetime of refresh tokens. Controls session persistence.                  |
| `cookie_name`                 | `str`                              | `"refresh_token"` | Cookie name used to store refresh tokens (optional).                       |
| `cookie_secure`               | `bool`                             | `True`            | Forces HTTPS-only cookie transmission.                                     |
| `cookie_httponly`             | `bool`                             | `True`            | Prevents JavaScript access to token cookie (XSS protection).               |
| `cookie_samesite`             | `Literal["strict", "lax", "none"]` | `"strict"`        | Controls cross-site cookie behavior (CSRF mitigation).                     |

---

## **Derived Attributes**

These values are automatically computed:

| Attribute              | Type        | Meaning                                    |
| ---------------------- | ----------- | ------------------------------------------ |
| `access_token_expire`  | `timedelta` | Exact duration for access token validity.  |
| `refresh_token_expire` | `timedelta` | Exact duration for refresh token validity. |

---

## **Security Recommendations**

| Environment                         | Recommended Settings                                          |
| ----------------------------------- | ------------------------------------------------------------- |
| Development                         | `cookie_secure=False`, `algorithm="HS256"`                    |
| Production                          | `cookie_secure=True`, HTTPS enforced, long secret or RSA keys |
| Distributed Systems / Microservices | Prefer `"RS256"` (public verification, private signing)       |

Additional best practices:

* Rotate refresh tokens.
* Never expose `secret_key` in logs or client-side code.
* Store secrets using environment variables or a vault.

---

## **Integration Flow**

```
AuthConfig → TokenService → AuthMiddleware / Dependency → API Routes
```

* `AuthConfig` defines the rules.
* Token service uses it to sign and validate JWTs.
* Middleware/dependencies enforce authentication on protected endpoints.

---

## **Serialization Behavior**

When converted to a dict, the secret key is replaced by its hash representation to avoid accidental exposure.

---

## **When to Customize**

Customize the configuration when:

* Deploying to multiple environments with different policies.
* Switching authentication algorithms.
* Adjusting session persistence duration.
* Enabling secure cookie-based refresh workflows.

---

## Summary

`AuthConfig` is the foundational configuration layer of the authentication module.
It ensures consistent behavior, security enforcement, and flexibility across different deployment models.

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
