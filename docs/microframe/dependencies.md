# Dependencies

Documentation for `microframe/dependencies/manager.py` - Dependency injection system.

## Depends

Mark a parameter as a dependency.

### Basic Usage

```python
from microframe import Depends

def get_db():
    return Database()

@app.get("/users")
async def list_users(db=Depends(get_db)):
    users = db.query("SELECT * FROM users")
    return {"users": users}
```

## Dependency Types

### Function Dependencies

```python
def get_current_user(token: str):
    user = verify_token(token)
    if not user:
        raise UnauthorizedException()
    return user

@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user
```

### Class Dependencies

```python
class Database:
    def __init__(self):
        self.connection = create_connection()
    
    def query(self, sql: str):
        return self.connection.execute(sql)

@app.get("/data")
async def get_data(db: Database = Depends(Database)):
    return db.query("SELECT * FROM data")
```

### Async Dependencies

```python
async def get_async_db():
    db = await connect_async_db()
    try:
        yield db
    finally:
        await db.close()

@app.get("/data")
async def get_data(db=Depends(get_async_db)):
    return await db.fetch_all()
```

## Nested Dependencies

```python
def get_db():
    return Database()

def get_user_repo(db=Depends(get_db)):
    return UserRepository(db)

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    repo=Depends(get_user_repo)
):
    return repo.get(user_id)
```

## Caching

```python
# Register with caching
app.register_dependency("db", get_db, cache=True)

# Dependency is created once and reused
```

---

## 📖 Navigation

**Documentation Modules Core** :
- [Index Modules](README.md)
- [Application](application.md)
- [Config](config.md)
- [Router](router.md)
- [Dependencies](dependencies.md)
- [Validation](validation.md)
- [Middleware](middleware.md)
- [Exceptions](exceptions.md)
- [Templates](templates.md)
- [UI Components](ui.md)
- [Configurations](configurations.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guides Pratiques](../guides/getting-started.md)**
