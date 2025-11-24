# 🎯 Best Practices - MicroFrame

> Guide des meilleures pratiques pour développer des applications robustes, performantes et sécurisées avec MicroFrame

## 📋 Structure de Projet

### Structure Recommandée

```
my-project/
├── app.py                      # Point d'entrée
├── config.py                   # Configuration centralisée
├── requirements.txt            # Dépendances
├── .env.example                # Template env vars
├── .gitignore                  # Git ignore
│
├── routes/                     # Routes organisées par domaine
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   └── items.py
│
├── models/                     # Modèles Pydantic
│   ├── __init__.py
│   ├── user.py
│   └── item.py
│
├── services/                   # Logique métier
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
│
├── database/                   # Database layer
│   ├── __init__.py
│   ├── models.py              # ORM models
│   └── session.py             # DB session
│
├── middlewares/                # Middlewares custom
│   └── custom_middleware.py
│
├── utils/                      # Utilitaires
│   ├── __init__.py
│   └── helpers.py
│
├── tests/                      # Tests
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_users.py
│
├── templates/                  # Templates (si applicable)
│   └── index.html
│
├── static/                     # Fichiers statiques
│   ├── css/
│   └── js/
│
└── docs/                       # Documentation projet
    └── API.md
```

---

## 🏗️ Architecture et Design

### Separation of Concerns

**✅ BON** - Séparation claire :
```python
# models/user.py - Validation seulement
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# services/user_service.py - Logique métier
class UserService:
    async def create_user(self, data: UserCreate):
        # Business logic here
        hashed = hash_password(data.password)
        return await db.create_user(...)

# routes/users.py - Routing seulement
@router.post("/users")
async def create_user(data: UserCreate, service = Depends(get_user_service)):
    return await service.create_user(data)
```

**❌ MAUVAIS** - Tout mélangé :
```python
@router.post("/users")
async def create_user(data: dict):
    # Validation manuelle
    if not data.get("email"):
        raise ValueError()
    
    # Business logic dans la route
    hashed = hash_password(data["password"])
    
    # DB access direct
    db.insert(...)
```

### Dependency Injection

**✅ BON** - Injectable et testable :
```python
def get_user_service(db = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)
```

---

## 🔒 Sécurité

### Password Security

**✅ BON** - Bcrypt avec salt :
```python
from microframe.authx.security import hash_password, verify_password

# Hash lors de la création
hashed = hash_password(plain_password)

# Verify lors du login
is_valid = verify_password(plain_password, hashed)
```

**❌ MAUVAIS** - SHA256 simple :
```python
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()  # ❌ Insecure!
```

### JWT Token Security

**✅ BON** - Tokens courts + refresh :
```python
auth_config = AuthConfig(
    secret_key=os.getenv("SECRET_KEY"),  # From env
    access_token_expire_minutes=15,      # Court!
    refresh_token_expire_days=7
)
```

**❌ MAUVAIS** - Token long :
```python
access_token_expire_minutes=86400  # ❌ 60 jours!
```

### Input Validation

**✅ BON** - Pydantic validation :
```python
class UpdateUser(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=0, le=150)
    email: EmailStr

@router.put("/users/{user_id}")
async def update_user(user_id: int, data: UpdateUser):
    # data est déjà validé!
    return await service.update(user_id, data)
```

### SQL Injection Protection

**✅ BON** - Parameterized queries :
```python
# Avec SQLAlchemy
query = select(User).where(User.email == email)

# Avec asyncpg
await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
```

**❌ MAUVAIS** - String interpolation :
```python
query = f"SELECT * FROM users WHERE email = '{email}'"  # ❌ SQL Injection!
```

---

## ⚡ Performance

### Async Everywhere

**✅ BON** - Async/await :
```python
@app.get("/users")
async def get_users(db = Depends(get_db)):
    # Non-bloquant
    users = await db.fetch_all("SELECT * FROM users")
    return users
```

**❌ MAUVAIS** - Sync bloquant :
```python
@app.get("/users")
def get_users():
    # ❌ Bloque l'event loop!
    users = sync_db.query("SELECT * FROM users")
    return users
```

###Connection Pooling

**✅ BON** - Pool de connexions :
```python
from databases import Database

database = Database(
    "postgresql://user:pass@localhost/db",
    min_size=5,
    max_size=20
)

# Startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

### Caching

**✅ BON** - Cache les données lourdes :
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_config():
    # Expensive config loading
    return load_config()

# Ou avec Redis
import aioredis

redis = await aioredis.create_redis_pool('redis://localhost')

async def get_user(user_id: int):
    # Try cache first
    cached = await redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # Query DB
    user = await db.get_user(user_id)
    
    # Cache for 5 minutes
    await redis.setex(f"user:{user_id}", 300, json.dumps(user))
    return user
```

### Pagination

**✅ BON** - Toujours paginer :
```python
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

@app.get("/users")
async def list_users(pagination: PaginationParams = Depends()):
    offset = (pagination.page - 1) * pagination.per_page
    users = await db.fetch_all(
        "SELECT * FROM users LIMIT $1 OFFSET $2",
        pagination.per_page,
        offset
    )
    return {"users": users, "page": pagination.page}
```

---

## 🧪 Testing

### Structure Tests

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_headers(client):
    # Login et retourner headers
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

```python
# tests/test_users.py
@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users", json={
        "email": "new@example.com",
        "password": "secret123",
        "name": "New User"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"

@pytest.mark.asyncio
async def test_get_protected_route(client, auth_headers):
    response = await client.get("/me", headers=auth_headers)
    assert response.status_code == 200
```

### Test Coverage

```bash
# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Objectif: 80%+ coverage
```

---

## 📝 Documentation

### Docstrings

**✅ BON** - Docstrings complètes :
```python
@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user account.
    
    Args:
        user: User data (email, password, name)
        service: User service dependency
    
    Returns:
        UserResponse: Created user data
    
    Raises:
        ValidationException: If email already exists
    """
    return await service.create_user(user)
```

### OpenAPI Documentation

**✅ BON** - Metadata complète :
```python
app = Application(
    title="Ma Super API",
    version="1.0.0",
    description="""
    ## Features
    * User management
    * Authentication JWT
    * WebSocket chat
    
    ## Authentication
    Use `/auth/login` to get access token
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)
```

---

## 🛡️ Error Handling

### Exceptions Typées

**✅ BON** - Exceptions claires :
```python
from microframe import NotFoundException, ValidationException

@router.get("/users/{user_id}")
async def get_user(user_id: int, service = Depends(get_user_service)):
    user = await service.get_user(user_id)
    
    if not user:
        raise NotFoundException(
            f"User with ID {user_id} not found",
            details={"user_id": user_id}
        )
    
    return user
```

### Logging

**✅ BON** - Logs structurés :
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/users")
async def create_user(user: UserCreate):
    logger.info(f"Creating user: {user.email}")
    
    try:
        created_user = await service.create_user(user)
        logger.info(f"User created: ID={created_user.id}")
        return created_user
    
    except Exception as e:
        logger.error(f"Failed to create user: {e}", exc_info=True)
        raise
```

---

## 🔐 Configuration

### Environment Variables

**✅ BON** - Toujours depuis env :
```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Secret Management

**✅ BON** - Secrets sécurisés :
```bash
# .env (gitignored!)
SECRET_KEY=generate-with-secrets-token-hex-32
DATABASE_URL=postgresql://user:pass@localhost/db

# .env.example (committed)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
```

---

## 📊 Monitoring

### Health Checks

```python
@app.get("/health")
async def health_check(db = Depends(get_db)):
    """Endpoint pour load balancers"""
    
    # Check database
    try:
        await db.fetch_one("SELECT 1")
        db_ok = True
    except:
        db_ok = False
    
    status = "healthy" if db_ok else "unhealthy"
    
    return {
        "status": status,
        "version": "1.0.0",
        "database": "ok" if db_ok else "error",
        "timestamp": datetime.now().isoformat()
    }
```

### Metrics

```python
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration'
)
```

---

## ✅ Checklist Finale

### Avant Commit
- [ ] Tests passent tous (`pytest`)
- [ ] Coverage > 80% (`pytest --cov`)
- [ ] Pas de secrets dans le code
- [ ] Code formaté (`black`, `isort`)
- [ ] Pas de linting errors (`flake8`, `mypy`)
- [ ] Docstrings à jour

### Avant Production
- [ ] DEBUG=false
- [ ] Secrets dans environnement
- [ ] HTTPS activé
- [ ] Rate limiting configuré
- [ ] Logs configurés
- [ ] Monitoring activé
- [ ] Backup strategy en place
- [ ] Load testing effectué

---

## 📖 Ressources

- **[Guide Deployment](deployment.md)** - Déploiement production
- **[Security Best Practices](https://cheatsheetseries.owasp.org/)**
- **[Python Best Practices](https://docs.python-guide.org/)**

---

---

## 📖 Navigation

**Parcours Documentation** :
1. [Index](../README.md)
2. [Getting Started](getting-started.md)
3. [Authentication](authentication.md)
4. [WebSocket Chat](websocket-chat.md)
5. [Deployment](deployment.md)
6. **📍 Best Practices** (vous êtes ici) - 🎓 **FIN DU PARCOURS**

---

## 🎓 Conclusion du Parcours

Félicitations ! Vous avez complété le parcours complet de la documentation MicroFrame.

**Vous maîtrisez maintenant** :
- ✅ Installation et concepts de base
- ✅ Authentification JWT avec AuthX
- ✅ WebSocket temps réel
- ✅ Déploiement production
- ✅ Best practices sécurité et performance

**Prochaines étapes recommandées** :
- 📚 Consulter la [documentation modules](../microframe/README.md) pour approfondir
- 🔧 Voir la [ROADMAP](../../ROADMAP.md) pour features à venir
- 💡 Contribuer sur [GitHub](https://github.com/traoreera/microframe)

---

**[← Deployment](deployment.md)** | **[↑ Retour à l'Index](../README.md)** | **[📚 Docs Modules →](../microframe/README.md)**
