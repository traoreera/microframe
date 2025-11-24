# 🔐 Guide Authentification - AuthX

> Guide complet pour ajouter l'authentification JWT à votre application MicroFrame avec le module AuthX

## 📋 Prérequis

- MicroFrame installé
- Compréhension des bases (voir [Getting Started](getting-started.md))
- Python 3.13+

---

## 📦 Installation AuthX

AuthX est un **module séparé optionnel** de MicroFrame.

```bash
# AuthX est déjà inclus dans le repo microframe
# Accessible via:
from microframe.authx import AuthConfig, AuthManager
```

### Dépendances Requises

AuthX utilise :
- **jose** - JWT encoding/decoding
- **bcrypt** - Password hashing
- **pydantic** - Validation

---

## 🚀 Mise en Place Rapide

### 1. Configuration AuthX

Créez `auth_config.py` :

```python
from microframe.authx import AuthConfig

# Configuration JWT
auth_config = AuthConfig(
    secret_key="votre-cle-secrete-min-32-caracteres",  # ⚠️ Changez ceci !
    algorithm="HS256",
    access_token_expire_minutes=15,
    refresh_token_expire_days=7
)
```

> **🔒 Sécurité** : Générez une clé secrète forte :
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

### 2. Implémenter AuthManager

Créez `auth_manager.py` :

```python
from microframe.authx import AuthManager, UserResponse
from microframe.authx.security import verify_password, hash_password

# Fake database pour l'exemple
fake_users_db = {
    "john@example.com": {
        "id": "1",
        "email": "john@example.com",
        "hashed_password": "$2b$12$...",  # bcrypt hash
        "name": "John Doe"
    }
}

class MyAuthManager(AuthManager):
    """AuthManager custom avec votre logique database"""
    
    async def get_user_by_email(self, email: str):
        """Récupère un user par email"""
        user_data = fake_users_db.get(email)
        if not user_data:
            return None
        
        return UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            data={"name": user_data["name"]}
        )
    
    async def get_user_by_id(self, user_id: str):
        """Récupère un user par ID"""
        for user_data in fake_users_db.values():
            if user_data["id"] == user_id:
                return UserResponse(
                    id=user_data["id"],
                    email=user_data["email"],
                    data={"name": user_data["name"]}
                )
        return None
    
    async def verify_password(self, email: str, password: str) -> bool:
        """Vérifie le mot de passe"""
        user_data = fake_users_db.get(email)
        if not user_data:
            return False
        
        return verify_password(password, user_data["hashed_password"])
```

---

### 3. Routes d'Authentification

Créez `routes/auth.py` :

```python
from microframe import Router
from microframe.authx import (
    create_access_token,
    create_refresh_token,
    TokenResponse,
    CredentialsException
)
from pydantic import BaseModel, EmailStr

router = Router(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenResponse)
async def login(request, credentials: LoginRequest, auth_manager, auth_config):
    """Login et retourne access + refresh tokens"""
    
    # Authentifier
    user = await auth_manager.authenticate(
        credentials.email,
        credentials.password
    )
    
    if not user:
        raise CredentialsException("Email ou mot de passe incorrect")
    
    # Créer tokens
    access_token = create_access_token(user.id, auth_config)
    refresh_token = create_refresh_token(user.id, auth_config)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
```

---

### 4. Application Principale

Dans `app.py` :

```python
from microframe import Application, AppConfig
from microframe.authx import AuthConfig
from auth_config import auth_config
from auth_manager import MyAuthManager
from routes.auth import router as auth_router

# Créer l'app
app = Application(
    AppConfig(
    title="API avec Authentification",
    version="1.0.0"
    )
)

# Injecter auth_config et auth_manager dans app.state
app.state.auth_config = auth_config
app.state.auth_manager = MyAuthManager()

# Inclure routes auth
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

---

## 🔐 Routes Protégées

### Avec get_current_user

```python
from microframe import Router, Depends
from microframe.authx import get_current_user, UserResponse

router = Router(prefix="/api", tags=["API"])

@router.get("/me")
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Route protégée - nécessite authentification"""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "name": current_user.data.get("name")
    }

@router.get("/profile")
async def get_profile(current_user: UserResponse = Depends(get_current_user)):
    """Autre route protégée"""
    return {"profile": current_user.dict()}
```

### Tester les Routes Protégées

```bash
# 1. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secret"}'

# Réponse:
# {
#   "access_token": "eyJhbGc...",
#   "refresh_token": "eyJhbGc...",
#   "token_type": "bearer"
# }

# 2. Accéder route protégée
curl http://localhost:8000/api/me \
  -H "Authorization: Bearer eyJhbGc..."

# Réponse:
# {
#   "user_id": "1",
#   "email": "john@example.com",
#   "name": "John Doe"
# }
```

---

## 👤 Register (Inscription)

### Route d'Inscription

```python
from microframe.authx.security import hash_password

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8)

@router.post("/register")
async def register(credentials: RegisterRequest, auth_manager):
    """Créer un nouveau compte"""
    
    # Vérifier si email existe déjà
    existing = await auth_manager.get_user_by_email(credentials.email)
    if existing:
        raise ValidationException("Email déjà utilisé")
    
    # Hasher le mot de passe
    hashed_password = hash_password(credentials.password)
    
    # Créer user (adapter à votre DB)
    user_id = str(len(fake_users_db) + 1)
    fake_users_db[credentials.email] = {
        "id": user_id,
        "email": credentials.email,
        "hashed_password": hashed_password,
        "name": credentials.name
    }
    
    # Retourner tokens directement (auto-login)
    access_token = create_access_token(user_id, app.state.auth_config)
    refresh_token = create_refresh_token(user_id, app.state.auth_config)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
```

---

## 🔄 Refresh Token

### Route Refresh

```python
from microframe.authx import decode_token, InvalidTokenException

@router.post("/refresh")
async def refresh_token(request, auth_config, auth_manager):
    """Rafraîchir l'access token"""
    
    # Récupérer refresh token (cookie ou body)
    refresh = request.cookies.get("refresh_token")
    if not refresh:
        # Ou depuis le body
        data = await request.json()
        refresh = data.get("refresh_token")
    
    if not refresh:
        raise CredentialsException("Refresh token manquant")
    
    try:
        # Valider refresh token
        payload = decode_token(refresh, auth_config, "refresh")
        user_id = payload.get("sub")
        
        # Vérifier que user existe toujours
        user = await auth_manager.get_user_by_id(user_id)
        if not user:
            raise CredentialsException("User invalide")
        
        # Créer nouveau access token
        new_access = create_access_token(user_id, auth_config)
        
        return {"access_token": new_access, "token_type": "bearer"}
        
    except (InvalidTokenException, TokenExpiredException):
        raise CredentialsException("Refresh token invalide ou expiré")
```

---

## 🗄️ Avec Base de Données Réelle

### Exemple SQLAlchemy

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from microframe.authx import AuthManager, UserResponse

# Engine async
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class DatabaseAuthManager(AuthManager):
    def __init__(self):
        self.session_factory = SessionLocal
    
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
                    data={"name": user.name, "role": user.role}
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
```

---

## 🔒 Sécurité Production

### Configuration Sécurisée

```python
# .env
SECRET_KEY=votre-cle-generee-avec-secrets-token-hex-32
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```

```python
# config.py
import os
from microframe.authx import AuthConfig

auth_config = AuthConfig(
    secret_key=os.getenv("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)),
    refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
)
```

### Checklist Sécurité

- ✅ Clé secrète forte (32+ caractères aléatoires)
- ✅ HTTPS en production
- ✅ Access token court (15-30 min)
- ✅ Refresh token plus long (7 jours)
- ✅ Password hashing avec bcrypt
- ✅ Rate limiting sur `/login`
- ✅ CORS configuré correctement
- ✅ Secrets dans variables d'environnement

---

## 📖 Prochaines Étapes

- **[WebSocket Chat](websocket-chat.md)** - Ajouter auth aux WebSockets
- **[Deployment](deployment.md)** - Déployer avec auth en production
- **[Best Practices](best-practices.md)** - Sécurité avancée

---

---

## 📖 Navigation

**Parcours Documentation** :
1. [Index](../README.md)
2. [Getting Started](getting-started.md)
3. **📍 Authentication** (vous êtes ici)
4. [WebSocket Chat](websocket-chat.md)
5. [Deployment](deployment.md)
6. [Best Practices](best-practices.md)

---

**[← Getting Started](getting-started.md)** | **[Index](../README.md)** | **[WebSocket Chat →](websocket-chat.md)**
