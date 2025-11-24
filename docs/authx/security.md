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

## 🔒 Password Utilities

This module provides secure password hashing and verification using **bcrypt**.
It is designed to ensure safe storage and validation of user credentials.

---

### 🛠 Functions

#### `hash_password(password: str) -> str`

Hashes a plaintext password using bcrypt.

**Parameters:**

* `password` — Plaintext password

**Returns:**

* `str` — Hashed password (UTF-8 encoded string)

**Example:**

```python
from authx.security import hash_password

hashed = hash_password("mysecretpassword")
print(hashed)
# $2b$12$...
```

---

#### `verify_password(plain_password: str, hashed_password: str) -> bool`

Checks if a plaintext password matches the stored hash.

**Parameters:**

* `plain_password` — Password provided by the user
* `hashed_password` — Stored bcrypt hash

**Returns:**

* `bool` — `True` if passwords match, `False` otherwise

**Example:**

```python
from authx.security import verify_password

is_valid = verify_password("mysecretpassword", hashed)
if is_valid:
    print("Password correct")
else:
    print("Invalid password")
```

---

### 🔐 Security Notes

* Always store only the hashed password in your database.
* Do **not** log plaintext passwords.
* Use `bcrypt` with default or higher work factor (`gensalt()` default is 12) for modern security.
* `verify_password()` handles exceptions safely, returning `False` for invalid input or corrupted hashes.

---

This module integrates seamlessly with `AuthManager`’s `verify_password()` method for authentication workflows.

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
