# Guide de Migration v1.0 → v2.0

Ce guide vous aide à migrer votre code de l'ancienne architecture vers la nouvelle architecture modulaire.

## Résumé des changements

### ✅ Ce qui reste identique
- Les décorateurs de routes (`@app.get`, `@app.post`, etc.)
- Le système `Depends()` pour l'injection de dépendances
- La validation Pydantic
- Les middlewares de base (CORS, Security)
- L'intégration avec Starlette et Uvicorn

### ⚠️ Ce qui change
- Structure des imports
- Noms de certaines classes (`APIRouter` → `Router`)
- Organisation des fichiers
- Gestion des exceptions

## Changements d'imports

### Avant (v1.0)
```python
from microframe.app import Application
from microframe.routing import APIRouter
from microframe.dependencies import Depends, AppException
from microframe.middleware.security import CORSMiddleware, SecurityMiddleware
```

### Après (v2.0)
```python
from microframe import Application, Router, Depends
from microframe import HTTPException  # Nouveau nom
from microframe.middleware import CORSMiddleware, SecurityMiddleware
```

## Changements de classes

### Router

**Avant:**
```python
from microframe.routing import APIRouter

router = APIRouter(prefix="/api", tags=["API"])
```

**Après:**
```python
from microframe import Router

router = Router(prefix="/api", tags=["API"])
```

### Exceptions

**Avant:**
```python
from microframe.dependencies import AppException

raise AppException("Error message", status_code=400)
```

**Après:**
```python
from microframe import HTTPException

raise HTTPException("Error message", status_code=400)
```

Nouvelles exceptions spécifiques:
```python
from microframe import (
    NotFoundException,      # 404
    UnauthorizedException,  # 401
    ForbiddenException,     # 403
    ValidationException     # 422
)
```

## Configuration

### Avant (v1.0)
```python
app = Application(
    title="My API",
    version="1.0.0",
    description="My description"
)
```

### Après (v2.0) - Option 1 (Simple)
```python
from microframe import Application

app = Application(
    title="My API",
    version="1.0.0",
    description="My description"
)
```

### Après (v2.0) - Option 2 (Avancé avec config)
```python
from microframe import Application
from microframe.core import AppConfig

config = AppConfig(
    title="My API",
    version="1.0.0",
    description="My description",
    debug=True,
    cors_origins=["http://localhost:3000"],
    rate_limit_requests=100
)

app = Application(config=config)
```

## Middlewares

### Avant (v1.0)
```python
from microframe.middleware.security import CORSMiddleware, SecurityMiddleware

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(SecurityMiddleware)
```

### Après (v2.0)
```python
from microframe.middleware import CORSMiddleware, SecurityMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)

app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,
    rate_limit_window=60
)
```

## Dépendances

Le système reste identique mais est maintenant plus optimisé:

```python
from microframe import Depends

def get_db():
    return Database()

@app.get("/users")
async def list_users(db=Depends(get_db)):
    return {"users": db.query_all()}
```

## Routes imbriquées

### Avant (v1.0)
```python
from microframe.routing import APIRouter

test = APIRouter(prefix="/v1", tags=["Test"])
test2 = APIRouter(prefix="/test", tags=["Another"])

test.include_router(test2)
app.include_router(router=test)
```

### Après (v2.0)
```python
from microframe import Router

test = Router(prefix="/v1", tags=["Test"])
test2 = Router(prefix="/test", tags=["Another"])

test.include_router(test2)
app.include_router(test)
```

## Exemple de migration complète

### Avant (v1.0)

```python
from microframe.app import Application
from microframe.routing import APIRouter
from microframe.dependencies import Depends, AppException
from microframe.middleware.security import CORSMiddleware

app = Application(title="Test API", version="1.0.0")

router = APIRouter(prefix="/api", tags=["API"])

def get_db():
    return {"db": "connection"}

@router.get("/users")
async def get_users(db=Depends(get_db)):
    if not db:
        raise AppException("DB error", status_code=500)
    return {"users": []}

app.include_router(router=router)
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

### Après (v2.0)

```python
from microframe import Application, Router, Depends, HTTPException
from microframe.middleware import CORSMiddleware

app = Application(title="Test API", version="1.0.0")

router = Router(prefix="/api", tags=["API"])

def get_db():
    return {"db": "connection"}

@router.get("/users")
async def get_users(db=Depends(get_db)):
    if not db:
        raise HTTPException("DB error", status_code=500)
    return {"users": []}

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)
```

## Nouvelles fonctionnalités

### 1. Configuration centralisée

```python
from microframe import Application
from microframe.core import AppConfig

config = AppConfig(
    title="My API",
    version="2.0.0",
    debug=True,
    docs_url="/docs",
    openapi_url="/openapi.json",
    cors_origins=["http://localhost:3000"],
    rate_limit_requests=100,
    rate_limit_window=60
)

app = Application(config=config)
```

### 2. Exceptions typées

```python
from microframe import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = db.get(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    return user

@app.get("/admin")
async def admin_panel(user=Depends(get_current_user)):
    if not user.is_admin:
        raise ForbiddenException("Admin access required")
    return {"admin": "panel"}
```

### 3. Registry des routes

```python
# Accéder à toutes les routes enregistrées
routes = app.route_registry.get_all()
for route in routes:
    print(f"{route.methods} {route.path} - {route.tags}")

# Filtrer par tag
api_routes = app.route_registry.get_by_tag("API")
```

## Checklist de migration

- [ ] Mettre à jour les imports
  - [ ] `APIRouter` → `Router`
  - [ ] `AppException` → `HTTPException`
  - [ ] Imports simplifiés depuis `microframe`
- [ ] Vérifier les middlewares
  - [ ] Imports depuis `microframe.middleware`
  - [ ] Configuration des paramètres
- [ ] Tester les routes
  - [ ] Vérifier les dépendances
  - [ ] Vérifier les exceptions
- [ ] Tester la documentation
  - [ ] `/docs` fonctionne
  - [ ] `/redoc` fonctionne
  - [ ] `/openapi.json` est valide
- [ ] Exécuter les tests
  - [ ] Tests unitaires
  - [ ] Tests d'intégration

## Bénéfices de la migration

✅ **Code plus propre**: Imports simplifiés et structure claire
✅ **Meilleures performances**: Cache optimisé et résolution plus rapide
✅ **Plus maintenable**: Modules séparés et testables
✅ **Plus extensible**: Architecture modulaire facile à étendre
✅ **Meilleure documentation**: Code autodocumenté

## Support

Si vous rencontrez des problèmes lors de la migration:

1. Consultez `ARCHITECTURE.md` pour comprendre la nouvelle structure
2. Regardez `examples/basic_app.py` pour des exemples complets
3. Vérifiez que toutes les dépendances sont à jour dans `pyproject.toml`

## Compatibilité

La version 2.0 maintient une API similaire à la v1.0, mais avec quelques breaking changes nécessaires pour améliorer l'architecture. Prenez le temps de tester votre application après migration.

### Versions supportées
- Python: 3.9+
- Starlette: 0.37+
- Pydantic: 2.6+
- Uvicorn: 0.29+
