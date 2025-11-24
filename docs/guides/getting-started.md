# 🚀 Guide de Démarrage - MicroFrame

> Guide complet pour démarrer avec MicroFrame v2.0 - De l'installation à votre première application

## 📋 Prérequis

-  **Python 3.13+** installé
- **pip** ou **poetry** pour la gestion des dépendances
- Éditeur de code (VSCode, PyCharm, etc.)

---

## 📦 Installation

### Méthode 1 : Depuis les sources (recommandé pour développement)

```bash
# Cloner le repository
git clone https://github.com/traoreera/microframe.git
cd microframe

# Installer en mode développement
pip install -e .

# Ou avec poetry
poetry install
```

### Méthode 2 : Avec pip (quand publié sur PyPI)

```bash
pip install microframe
```

### Vérification

```bash
python -c "import microframe; print(microframe.__version__)"
# Devrait afficher: 2.0.0
```

---

## 🎯 Votre Première Application

### 1. Application Minimale

Créez `app.py` :

```python
from microframe import Application

# Créer l'application
app = Application(
    title="Ma Première API",
    version="1.0.0",
    description="Une API simple avec MicroFrame"
)

# Route simple
@app.get("/")
async def index():
    return {"message": "Hello, MicroFrame!"}

# Route avec paramètre
@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f "Bonjour, {name}!"}

# Lancer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### 2. Lancer l'application

```bash
python app.py
```

### 3. Tester

Ouvrez votre navigateur :
- **Application** : http://localhost:8000/
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI Schema** : http://localhost:8000/openapi.json

Avec curl :
```bash
curl http://localhost:8000/
# {"message": "Hello, MicroFrame!"}

curl http://localhost:8000/hello/John
# {"message": "Bonjour, John!"}
```

---

## 🛣️ Routes et Méthodes HTTP

### Toutes les méthodes HTTP

```python
from microframe import Application

app = Application()

@app.get("/items")
async def list_items():
    return {"items": []}

@app.post("/items")
async def create_item():
    return {"created": True}

@app.put("/items/{item_id}")
async def update_item(item_id: int):
    return {"updated": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"deleted": item_id}

@app.patch("/items/{item_id}")
async def partial_update(item_id: int):
    return {"patched": item_id}
```

### Paramètres de Route

```python
# Paramètre de chemin
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# Query parameters
@app.get("/search")
async def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}
# GET /search?q=python&limit=5

# Multi-paramètres
@app.get("/items/{category}/{item_id}")
async def get_item(category: str, item_id: int, details: bool = False):
    return {
        "category": category,
        "item_id": item_id,
        "details": details
    }
```

---

## ✅ Validation avec Pydantic

### Validation du Body

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
    is_active: bool = True

@app.post("/users")
async def create_user(user: User):
    # user est automatiquement validé
    return {
        "message": "User created",
        "user": user.dict()
    }
```

Test:
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }'
```

### Validation des Query Parameters

```python
from typing import Optional
from pydantic import BaseModel

class SearchParams(BaseModel):
    q: str
    category: Optional[str] = None
    min_price: float = 0
    max_price: float = 1000

@app.get("/products/search")
async def search_products(params: SearchParams):
    return {
        "query": params.q,
        "filters": {
            "category": params.category,
            "price_range": [params.min_price, params.max_price]
        }
    }
```

---

## 💉 Injection de Dépendances

### Dépendance Simple

```python
from microframe import Application, Depends

def get_current_user():
    # Simuler récupération user
    return {"id": "123", "username": "john"}

@app.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {"user": user}
```

### Dépendance avec Paramètres

```python
def get_database():
    # Simuler connexion DB
    db = {"type": "postgres", "connected": True}
    return db

def get_limit(limit: int = 10):
    return limit

@app.get("/users")
async def list_users(
    db=Depends(get_database),
    limit=Depends(get_limit)
):
    return {
        "database": db,
        "limit": limit,
        "users": []
    }
```

### Dépendances Imbriquées

```python
def get_db():
    return {"type": "postgres"}

def get_current_user(db=Depends(get_db)):
    # Utilise la dépendance db
    return {"id": "123", "from_db": db["type"]}

@app.get("/profile")
async def profile(user=Depends(get_current_user)):
    return {"user": user}
```

---

## 🛣️ Organisation avec Routers

### Router Modulaire

Créez `routes/users.py` :

```python
from microframe import Router
from pydantic import BaseModel

router = Router(prefix="/users", tags=["Users"])

class User(BaseModel):
    name: str
    email: str

@router.get("/")
async def list_users():
    return {"users": []}

@router.post("/")
async def create_user(user: User):
    return {"user": user.dict()}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

Dans `app.py` :

```python
from microframe import Application
from routes.users import router as users_router

app = Application()

# Inclure le router
app.include_router(users_router)

# Les routes deviennent:
# GET  /users/
# POST /users/
# GET  /users/{user_id}
```

### Router Imbriqués

```python
# API v1
api_v1 = Router(prefix="/api/v1", tags=["API v1"])

# Routers spécifiques
users_router = Router(prefix="/users", tags=["Users"])
items_router = Router(prefix="/items", tags=["Items"])

# Inclure dans v1
api_v1.include_router(users_router)
api_v1.include_router(items_router)

# Inclure dans l'app
app.include_router(api_v1)

# Routes finales:
# /api/v1/users/
# /api/v1/items/
```

---

## 🔒 Middleware

### CORS

```python
from microframe import Application
from microframe.middleware import CORSMiddleware

app = Application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True
)
```

### Security et Rate Limiting

```python
from microframe.middleware import SecurityMiddleware

app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,  # 100 requêtes
    rate_limit_window=60       # par minute
)
```

---

## ⚠️ Gestion des Erreurs

### Exceptions Typées

```python
from microframe import (
    NotFoundException,
    UnauthorizedException,
    ValidationException
)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Simuler recherche
    user = None  # Pas trouvé
    
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    
    return {"user": user}
```

### Handler d'Exceptions Custom

```python
from microframe import Application, HTTPException
from starlette.responses import JSONResponse

app = Application()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "path": request.url.path,
            "method": request.method
        }
    )
```

---

## 📚 Structure de Projet Recommandée

```
my-project/
├── app.py                 # Point d'entrée
├── config.py              # Configuration
├── requirements.txt       # Dépendances
├── routes/                # Routers
│   ├── __init__.py
│   ├── users.py
│   └── items.py
├── models/                # Modèles Pydantic
│   ├── __init__.py
│   └── user.py
├── services/              # Logique métier
│   └── user_service.py
└── tests/                 # Tests
    └── test_users.py
```

### Exemple Complet

**`models/user.py`** :
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
```

**`routes/users.py`** :
```python
from microframe import Router
from models.user import UserCreate, UserResponse

router = Router(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Logique de création
    return {
        "id": 1,
        "name": user.name,
        "email": user.email
    }
```

**`app.py`** :
```python
from microframe import Application
from routes.users import router as users_router

app = Application(
    title="My API",
    version="1.0.0"
)

app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🧪 Tests

```python
import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "secret123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
```

---

## 📖 Prochaines Étapes

Maintenant que vous maîtrisez les bases :

1. **[Authentication](authentication.md)** - Ajouter l'authentification avec AuthX
2. **[WebSocket](websocket-chat.md)** - Créer un chat temps réel
3. **[Deployment](deployment.md)** - Déployer en production
4. **[Best Practices](best-practices.md)** - Optimiser votre code

---

## 🔗 Ressources

- **[Documentation Complète](../README.md)** - Index de toute la documentation
- **[Exemples](../../examples/)** - Applications complètes
- **[API Reference](../microframe/README.md)** - Référence détaillée

---

---

## 📖 Navigation

**Parcours Documentation** :
1. [Index](../README.md)
2. **📍 Getting Started** (vous êtes ici)
3. [Authentication](authentication.md)
4. [WebSocket Chat](websocket-chat.md)
5. [Deployment](deployment.md)
6. [Best Practices](best-practices.md)

---

**[← Index](../README.md)** | **[Authentification →](authentication.md)**
