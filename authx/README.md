# Starlette AuthX

Module d'authentification JWT modulaire et réutilisable pour Starlette.

## Installation du module

### Depuis PyPI (après publication)

```bash
pip install starlette-authx
```

### Depuis les sources

```bash
# Cloner le repo
git clone https://github.com/yourusername/starlette-authx.git
cd starlette-authx

# Installer en mode développement
pip install -e .
```

## Utilisation rapide avec Cookiecutter

### Pré-requis

```bash
pip install cookiecutter
```

### Créer un nouveau projet

```bash
# Utiliser le template cookiecutter
cookiecutter gh:yourusername/cookiecutter-starlette-authx

# Ou depuis le dossier local
cookiecutter cookiecutter-starlette-authx/
```

Répondez aux questions :
- `project_name`: Mon API Starlette
- `project_slug`: mon_api_starlette (auto-généré)
- `project_description`: Une API avec authentification
- `author_name`: Votre Nom
- `author_email`: vous@example.com
- `python_version`: 3.11
- `use_docker`: yes/no

### Démarrer le projet

```bash
cd mon_api_starlette

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditez .env et changez SECRET_KEY

# Lancer l'application
python app.py
```

L'API est accessible sur `http://localhost:8000`

## Tester avec curl

### 1. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Réponse :
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

Le `refresh_token` est également stocké dans un cookie HttpOnly.

### 2. Récupérer les informations utilisateur

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer eyJhbGc..."
```

Réponse :
```json
{
  "id": "1",
  "email": "admin@example.com",
  "data": {
    "name": "Admin User",
    "role": "admin"
  }
}
```

### 3. Rafraîchir le token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Cookie: refresh_token=eyJhbGc..." \
  -c cookies.txt
```

Ou si vous avez sauvegardé les cookies lors du login :

```bash
# Lors du login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' \
  -c cookies.txt

# Puis refresh
curl -X POST http://localhost:8000/auth/refresh \
  -b cookies.txt
```

Réponse :
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## Utilisation manuelle (sans Cookiecutter)

### Installation

```bash
pip install starlette-authx uvicorn
```

### Code minimal

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from authx import (
    AuthConfig,
    AuthManager,
    create_auth_routes,
    AuthException,
    hash_password,
    verify_password,
)
from authx.models import UserResponse

# Implémenter votre AuthManager
class MyAuthManager(AuthManager):
    async def get_user_by_email(self, email: str):
        # Votre logique ici
        pass
    
    async def get_user_by_id(self, user_id: str):
        # Votre logique ici
        pass
    
    async def verify_password(self, email: str, password: str) -> bool:
        # Votre logique ici
        pass

# Configuration
auth_config = AuthConfig(
    secret_key="votre-cle-secrete-min-32-caracteres",
)
auth_manager = MyAuthManager()

# Application
routes = [
    Route("/", lambda r: JSONResponse({"message": "Hello"})),
    *create_auth_routes(),
]

app = Starlette(
    routes=routes,
    exception_handlers={
        AuthException: lambda r, e: JSONResponse(
            {"detail": e.message}, 
            status_code=e.status_code
        ),
    },
)

app.state.auth_config = auth_config
app.state.auth_manager = auth_manager
```

## Exemple avec base de données SQLAlchemy

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from authx import AuthManager, UserResponse, verify_password

class SQLAlchemyAuthManager(AuthManager):
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def get_user_by_email(self, email: str):
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            if user:
                return UserResponse(
                    id=str(user.id),
                    email=user.email,
                    data={"name": user.name}
                )
        return None
    
    async def get_user_by_id(self, user_id: str):
        async with self.session_factory() as session:
            user = await session.get(User, int(user_id))
            if user:
                return UserResponse(
                    id=str(user.id),
                    email=user.email,
                    data={"name": user.name}
                )
        return None
    
    async def verify_password(self, email: str, password: str) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            if user:
                return verify_password(password, user.hashed_password)
        return False

# Configuration
engine = create_async_engine("postgresql+asyncpg://...")
SessionLocal = sessionmaker(engine, class_=AsyncSession)
auth_manager = SQLAlchemyAuthManager(SessionLocal)
```

## Routes protégées

```python
from starlette.routing import Route
from authx import Depends, get_current_user
from authx.models import UserResponse
from authx.dependencies import resolve_dependencies

async def protected_route(request, current_user: UserResponse = Depends(get_current_user)):
    kwargs = await resolve_dependencies(request, protected_route)
    user = kwargs.get("current_user")
    
    return JSONResponse({
        "message": f"Hello {user.email}",
        "user": user.model_dump()
    })

routes = [
    Route("/protected", protected_route, methods=["GET"]),
    *create_auth_routes(),
]
```

## Configuration avancée

```python
auth_config = AuthConfig(
    secret_key="votre-cle-secrete-min-32-caracteres",
    algorithm="HS256",  # ou "RS256"
    access_token_expire_minutes=15,
    refresh_token_expire_days=7,
    cookie_name="refresh_token",
    cookie_secure=True,  # Active en production avec HTTPS
    cookie_httponly=True,
    cookie_samesite="strict",  # "strict", "lax", ou "none"
)
```

## Sécurité en production

### Variables d'environnement

```bash
# .env
SECRET_KEY=genere-avec-openssl-rand-hex-32
COOKIE_SECURE=true
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Générer une clé secrète

```bash
# Avec OpenSSL
openssl rand -hex 32

# Avec Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Checklist production

- ✅ `SECRET_KEY` long et aléatoire (min 32 caractères)
- ✅ `COOKIE_SECURE=true` (nécessite HTTPS)
- ✅ `cookie_samesite="strict"`
- ✅ CORS configuré correctement (`ALLOWED_ORIGINS`)
- ✅ Base de données persistante (pas in-memory)
- ✅ HTTPS activé
- ✅ Rate limiting sur `/auth/login`

## Architecture du module

```
authx/
├── __init__.py          # Exports publics
├── config.py            # Configuration AuthConfig
├── jwt.py               # Création/validation JWT
├── models.py            # Modèles Pydantic
├── manager.py           # AuthManager abstrait
├── dependencies.py      # Système Depends()
├── security.py          # Hash/vérification password
├── exceptions.py        # Exceptions custom
└── routes.py            # Routes d'authentification
```

## Développement

### Installation en mode dev

```bash
git clone https://github.com/yourusername/starlette-authx.git
cd starlette-authx
pip install -e ".[dev]"
```

### Tests

```bash
pytest
```

### Lancer l'exemple

```bash
cd example
pip install -r requirements.txt
python app.py
```

## License

MIT