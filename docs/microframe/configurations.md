# ⚙️ Configuration Modulaire

> Documentation du système de configuration modulaire de MicroFrame

## 📋 Vue d'ensemble

MicroFrame intègre un système de configuration modulaire permettant :
- ✅ Configuration par environnement (dev, staging, production)
- ✅ Validation automatique avec Pydantic
- ✅ Variables d'environnement (.env)
- ✅ Configuration hiérarchique
- ✅ Hot reload (optionnel)

---

## 🚀 Configuration de Base

### AppConfig

```python
from microframe import AppConfig, Application

config = AppConfig(
    title="Mon API",
    version="1.0.0",
    description="Description de l'API",
    debug=False,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app = Application(configuration=config)
```

### Paramètres AppConfig

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `title` | str | "MicroFrame App" | Titre de l'application |
| `version` | str | "1.0.0" | Version |
| `description` | str | "" | Description OpenAPI |
| `debug` | bool | False | Mode debug |
| `docs_url` | str | "/docs" | URL Swagger UI |
| `redoc_url` | str | "/redoc" | URL ReDoc |
| `openapi_url` | str | "/openapi.json" | URL schéma OpenAPI |
| `middleware` | list | [] | Liste middlewares |

---

## 📦 Module Configurations

### Structure

```python
from microframe.configurations import (
    BaseConfig,           # Configuration de base
    ConfigManager,        # Gestionnaire de config
    MicroFrameConfig,     # Config du framework
    JWTConfig,           # Config JWT
    SecurityConfig        # Config sécurité
)
```

### BaseConfig

```python
from microframe.configurations import BaseConfig

class DatabaseConfig(BaseConfig):
    """Configuration database"""
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str
    password: str
    pool_size: int = 10
    
    class Config:
        env_prefix = "DB_"  # Préfixe variables d'env

# Utilisation
db_config = DatabaseConfig(
    username="user",
    password="secret"
)

# Depuis variables d'env
# DB_USERNAME=user
# DB_PASSWORD=secret
db_config = DatabaseConfig()
```

---

## 🔧 ConfigManager

### Utilisation

```python
from microframe.configurations import ConfigManager

# Créer le manager
config_manager = ConfigManager()

# Enregistrer des configs
config_manager.register("database", DatabaseConfig())
config_manager.register("redis", RedisConfig())
config_manager.register("email", EmailConfig())

# Récupérer une config
db_config = config_manager.get("database")
redis_config = config_manager.get("redis")
```

### Charger depuis Fichier

```python
# config.json
{
    "database": {
        "host": "localhost",
        "port": 5432,
        "database": "myapp_prod",
        "username": "admin",
        "password": "secret",
        "pool_size": 20
    },
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0
    }
}
```

```python
# Charger depuis JSON
config_manager.load_from_file("config.json")

# Ou depuis YAML
config_manager.load_from_file("config.yaml")

# Ou depuis TOML
config_manager.load_from_file("config.toml")
```

---

## 🌍 Configuration par Environnement

### Structure de Fichiers

```
my-project/
├── config/
│   ├── base.py           # Config de base
│   ├── development.py    # Config dev
│   ├── staging.py        # Config staging
│   └── production.py     # Config production
├── .env.development
├── .env.staging
├── .env.production
└── app.py
```

### config/base.py

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuration de base"""
    app_name: str = "Mon API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    allowed_hosts: list[str] = ["*"]
    
    # API
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

### config/development.py

```python
from .base import Settings

class DevelopmentSettings(Settings):
    """Config pour développement"""
    debug: bool = True
    database_url: str = "sqlite:///./dev.db"
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    
    class Config:
        env_file = ".env.development"
```

### config/production.py

```python
from .base import Settings

class ProductionSettings(Settings):
    """Config pour production"""
    debug: bool = False
    database_url: str  # Doit être fourni
    
    # Sécurité renforcée
    allowed_hosts: list[str]  # Pas de "*"
    
    class Config:
        env_file = ".env.production"
```

### Chargement Conditionnel

```python
import os
from config.base import Settings
from config.development import DevelopmentSettings
from config.production import ProductionSettings

# Déterminer l'environnement
ENV = os.getenv("APP_ENV", "development")

# Charger la config appropriée
if ENV == "production":
    settings = ProductionSettings()
elif ENV == "staging":
    settings = StagingSettings()
else:
    settings = DevelopmentSettings()

# Validation
assert settings.secret_key, "SECRET_KEY must be set"
if not settings.debug:
    assert settings.database_url.startswith("postgresql://"), "Production needs PostgreSQL"
```

---

## 🔐 Configuration JWT (AuthX)

### JWTConfig

```python
from microframe.configurations import JWTConfig

jwt_config = JWTConfig(
    secret_key="votre-cle-secrete",
    algorithm="HS256",
    access_token_expire_minutes=15,
    refresh_token_expire_days=7
)
```

### Depuis Variables d'Env

```bash
# .env
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

```python
from microframe.authx import AuthConfig
import os

auth_config = AuthConfig(
    secret_key=os.getenv("JWT_SECRET_KEY"),
    algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 15)),
    refresh_token_expire_days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))
)
```

---

## 🔒 Configuration Sécurité

### SecurityConfig

```python
from microframe.configurations import SecurityConfig

security_config = SecurityConfig(
    rate_limit_requests=100,
    rate_limit_window=60,
    max_request_size=10_000_000,  # 10MB
    allowed_methods=["GET", "POST", "PUT", "DELETE"],
    cors_origins=["http://localhost:3000"]
)
```

---

## 💾 Gestion des Secrets

### Avec python-dotenv

```bash
# Install
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

# Charger .env
load_dotenv()

# Accéder aux secrets
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Avec Secrets Manager (Production)

```python
import boto3
import json

def get_secret(secret_name):
    """Récupérer secret depuis AWS Secrets Manager"""
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Utilisation
secrets = get_secret('myapp/production')
DATABASE_URL = secrets['database_url']
SECRET_KEY = secrets['secret_key']
```

---

## ✅ Validation de Configuration

### Validation Pydantic

```python
from pydantic import BaseSettings, validator, Field

class AppSettings(BaseSettings):
    database_url: str = Field(..., min_length=10)
    secret_key: str = Field(..., min_length=32)
    debug: bool = False
    
    @validator('database_url')
    def validate_database_url(cls, v):
        """Valider format database URL"""
        if not v.startswith(('postgresql://', 'mysql://', 'sqlite://')):
            raise ValueError('Invalid database URL scheme')
        return v
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Valider longueur secret key"""
        if len(v) < 32:
            raise ValueError('Secret key too short (min 32 chars)')
        return v
    
    @validator('debug')
    def validate_production(cls, v, values):
        """Vérifier qu'on n'est pas en debug en production"""
        if v and os.getenv('APP_ENV') == 'production':
            raise ValueError('Debug cannot be True in production')
        return v
```

---

## 🔄 Configuration Dynamique

### Hot Reload

```python
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigReloader(FileSystemEventHandler):
    def __init__(self, config_manager, config_file):
        self.config_manager = config_manager
        self.config_file = config_file
    
    def on_modified(self, event):
        if event.src_path == self.config_file:
            print(f"Reloading config from {self.config_file}")
            self.config_manager.load_from_file(self.config_file)

# Activer hot reload
observer = Observer()
observer.schedule(
    ConfigReloader(config_manager, "config.json"),
    path=".",
    recursive=False
)
observer.start()
```

---

## 📖 Exemple Complet

### Configuration Complète Application

```python
# config.py
import os
from pydantic import BaseSettings
from microframe import AppConfig
from microframe.authx import AuthConfig

class Settings(BaseSettings):
    # App
    app_name: str = "Mon API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    cors_origins: list[str] = ["http://localhost:3000"]
    
    # JWT
    jwt_algorithm: str = "HS256"
    jwt_access_expire_min: int = 15
    jwt_refresh_expire_days: int = 7
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    class Config:
        env_file = f".env.{os.getenv('APP_ENV', 'development')}"

# Load settings
settings = Settings()

# MicroFrame AppConfig
app_config = AppConfig(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None
)

# AuthX Config
auth_config = AuthConfig(
    secret_key=settings.secret_key,
    algorithm=settings.jwt_algorithm,
    access_token_expire_minutes=settings.jwt_access_expire_min,
    refresh_token_expire_days=settings.jwt_refresh_expire_days
)
```

### Utilisation dans App

```python
# app.py
from microframe import Application
from config import app_config, auth_config, settings

app = Application(configuration=app_config)

# Inject configs
app.state.settings = settings
app.state.auth_config = auth_config

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
```

---

## 📖 Ressources

- **[Pydantic Settings](https://docs.pydantic.dev/latest/usage/settings/)** - Documentation Pydantic
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Gestion .env
- **[Best Practices Guide](../guides/best-practices.md)** - Best practices configuration

---

---

## 📖 Navigation Modules

**Documentation Modules** :
- [Index Modules](README.md)
- [Templates](templates.md)
- **📍 Configurations** (vous êtes ici)
- [UI Components](ui.md)

---

**[↑ Index Principal](../README.md)** | **[← Templates](templates.md)** | **[UI Components →](ui.md)**
