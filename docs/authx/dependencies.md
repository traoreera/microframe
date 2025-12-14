# AuthX Dependencies

This section describes the dependency functions provided by the `authx` module.

---

## `get_current_user`

The `get_current_user` dependency is used to protect routes and get the current authenticated user.
It retrieves the user from the access token sent in the `Authorization` header.

### Usage

To use it, you need to inject it into your route handler using `microframe.Depends`.

```python
from microframe import Application, Depends, UserResponse, get_current_user

app = Application()

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
```

### How it works

1.  It expects an `Authorization` header with a `Bearer` token.
2.  It decodes the token and extracts the user ID (`sub` claim).
3.  It uses the `AuthManager` to retrieve the user from the database.
4.  It returns a `UserResponse` object.

### Exceptions

- `CredentialsException`: If the token is invalid, missing, or the user is not found.
- `UserNotFoundException`: If the user does not exist in the database.
