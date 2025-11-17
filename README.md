# 🚀 MicroFrame v2.0 - Architecture Modulaire

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MicroFramework v2.0** est un micro-framework ASGI moderne avec une architecture modulaire optimisée, inspiré de FastAPI.

## ✨ Nouveautés v2.0

- 🎯 **Architecture modulaire** - Code organisé en modules indépendants
- ⚡ **Performance optimisée** - Cache intelligent et résolution rapide
- 🔧 **Configuration centralisée** - `AppConfig` pour toute la configuration
- 🧪 **Testabilité améliorée** - Modules indépendants faciles à tester
- 📚 **Documentation complète** - Guides et exemples détaillés
- 🔒 **Exceptions typées** - `NotFoundException`, `UnauthorizedException`, etc.

## 📦 Installation rapide

```bash
git clone https://github.com/traoreera/microframe.git
cd microframework
pip install -e . 
#or
poetry init 
poetry add git+https://github.com/traoreera/microframe.git
#or
python -m venv .env
source .env/bin/activate
pip install git+https://github.com/traoreera/microframe.git
```

## 🚀 Démarrage rapide

### Application simple

```python
from microframe import Application

app = Application(
    title="My API",
    version="1.0.0",
    description="A simple API"
)

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id, "name": "John"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Avec routers modulaires

```python
from microframe import Application, Router
from pydantic import BaseModel

# Définir un modèle
class User(BaseModel):
    name: str
    email: str
    age: int

# Créer un router
users_router = Router(prefix="/users", tags=["Users"])

@users_router.get("/")
async def list_users():
    return {"users": [{"id": 1, "name": "Alice"}]}

@users_router.post("/")
async def create_user(user: User):
    return {"message": "User created", "user": user}

# Application
app = Application(title="Modular API")
app.include_router(users_router)
```

### Avec injection de dépendances

```python
from microframe import Application, Depends

def get_database():
    return {"type": "postgres", "connected": True}

@app.get("/data")
async def get_data(db=Depends(get_database)):
    return {"data": "...", "database": db}
```

### Avec middlewares

```python
from microframe import Application
from microframe.middleware import CORSMiddleware, SecurityMiddleware

app = Application()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)

# Security & Rate Limiting
app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,
    rate_limit_window=60
)
```

## 📁 Architecture

```
microframe/
├── core/               # Module central
│   ├── application.py  # Application principale
│   ├── config.py       # Configuration
│   └── exceptions.py   # Exceptions
│
├── http/               # Gestion HTTP
│   └── handlers.py     # Gestionnaires
│
├── routing/            # Système de routing
│   ├── router.py       # Router principal
│   ├── models.py       # Modèles
│   └── registry.py     # Registre
│
├── dependencies/       # Injection de dépendances
│   ├── manager.py      # Gestionnaire
│   └── models.py       # Depends
│
├── validation/         # Validation
│   └── parser.py       # Parser de requêtes
│
├── middleware/         # Middlewares
│   ├── cors.py         # CORS
│   └── security_middleware.py  # Security
│
└── docs/               # Documentation
    ├── openapi.py      # Générateur OpenAPI
    └── ui.py           # Swagger/ReDoc UI
```

## 🎓 Exemples

Consultez `examples/basic_app.py` pour un exemple complet avec:
- Routes modulaires avec routers
- Validation Pydantic
- Injection de dépendances
- Middlewares (CORS, Security)
- Routes imbriquées

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Guide complet de l'architecture
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migration depuis v1.0
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Résumé des changements

## 🔄 Migration depuis v1.0

### Changements principaux

```python
# Avant (v1.0)
from microframe.app import Application
from microframe.routing import APIRouter
from microframe.dependencies import AppException

# Après (v2.0)
from microframe import Application, Router, HTTPException
```

Voir [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) pour le guide complet.

## 🌟 Fonctionnalités

### ✅ Validation automatique avec Pydantic
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    title: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)

@app.post("/items")
async def create_item(item: Item):
    return {"item": item}
```

### ✅ Documentation auto-générée
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### ✅ Gestion d'erreurs typée
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
```

### ✅ Configuration centralisée
```python
from microframe.core import AppConfig

config = AppConfig(
    title="My API",
    version="2.0.0",
    debug=True,
    cors_origins=["http://localhost:3000"],
    rate_limit_requests=100,
    rate_limit_window=60,
    max_request_size=10_000_000
)

app = Application(config=config)
```

## 🧪 Tests

```bash
# Lancer les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=microframe --cov-report=html
```

## 🔒 Sécurité

- ✅ **Rate Limiting** - Protection contre les abus
- ✅ **CORS** - Configuration flexible
- ✅ **Security Headers** - X-Frame-Options, CSP, HSTS
- ✅ **Payload Validation** - Limitation de taille
- ✅ **Method Validation** - Méthodes HTTP autorisées

## 📊 Performance

- ⚡ **Cache intelligent** pour les dépendances
- ⚡ **Registry indexé** pour les routes (O(1))
- ⚡ **Imports lazy** pour un démarrage rapide
- ⚡ **Résolution optimisée** des dépendances

## 🛠️ Développement

```bash
# Installation en mode dev
pip install -e ".[dev]"

# Lancer l'application
python examples/basic_app.py

# Format du code
black microframe/

# Vérification du code
flake8 microframe/
mypy microframe/
```

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

MIT License - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- Inspiré par [FastAPI](https://fastapi.tiangolo.com/)
- Construit avec [Starlette](https://www.starlette.io/)
- Validation avec [Pydantic](https://pydantic-docs.helpmanual.io/)

## 📞 Contact

- GitHub: [@traoreera](https://github.com/traoreera)
- Documentation: [microframe.dev](https://microframe.dev)

---

⭐ **N'oubliez pas de mettre une étoile si ce projet vous aide !**
