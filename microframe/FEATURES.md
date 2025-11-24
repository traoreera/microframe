# MicroFrame v2.0 - Liste Complète des Fonctionnalités

> Framework ASGI moderne et complet pour Python 3.13+

## 🚀 Vue d'ensemble

MicroFrame v2.0 est un framework web ASGI complet offrant une architecture modulaire avec routing avancé, injection de dépendances, validation automatique, moteur de templates, composants UI, et bien plus.

---

## 📋 Table des matières

- [Core Framework](#-core-framework)
- [Routing](#-routing)
- [Injection de Dépendances](#-injection-de-dépendances)
- [Validation](#-validation)
- [Middleware et Sécurité](#-middleware-et-sécurité)
- [Documentation Automatique](#-documentation-automatique)
- [Moteur de Templates](#-moteur-de-templates)
- [Composants UI](#-composants-ui)
- [Configuration](#-configuration)
- [Utilitaires](#-utilitaires)
- [Testing](#-testing)

---

## 🎯 Core Framework

### Application ASGI
- ✅ **Compatible ASGI 3.0** - Basé sur Starlette pour performance maximale
- ✅ **Configuration centralisée** - Gestion de configuration via `AppConfig`
- ✅ **Hot reload** - Rechargement automatique en mode développement
- ✅ **Lazy loading** - Import des modules à la demande
- ✅ **Gestion d'événements** - Hooks de startup/shutdown
- ✅ **Mode debug** - Traces détaillées et messages d'erreur explicites

### Gestion des Exceptions
- ✅ **Exceptions typées** - `HTTPException`, `ValidationException`, `NotFoundException`, etc.
- ✅ **Handlers personnalisables** - Créez vos propres gestionnaires d'erreurs
- ✅ **Réponses JSON structurées** - Format cohérent pour toutes les erreurs
- ✅ **Status codes HTTP** - Support complet des codes HTTP standard

```python
from microframe import Application, NotFoundException

app = Application(title="Mon API", version="1.0.0")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if not user_exists(user_id):
        raise NotFoundException(f"User {user_id} not found")
    return {"user_id": user_id}
```

---

## 🛣️ Routing

### Routes HTTP
- ✅ **Méthodes HTTP** - GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD
- ✅ **Décorateurs intuitifs** - `@app.get()`, `@app.post()`, etc.
- ✅ **Route parameters** - Paramètres de chemin dynamiques
- ✅ **Query parameters** - Paramètres de requête automatiques
- ✅ **Request body** - Parsing automatique JSON/Form
- ✅ **File uploads** - Support des fichiers multipart/form-data

### Router Modulaire
- ✅ **Routers imbriqués** - Organisation hiérarchique des routes
- ✅ **Préfixes de routes** - Groupement logique avec préfixes
- ✅ **Tags** - Catégorisation des routes pour documentation
- ✅ **Middleware par router** - Middleware spécifique à un groupe
- ✅ **Inclusion de routers** - Composition de routers multiples

### Registry des Routes
- ✅ **Indexation O(1)** - Accès ultra-rapide aux routes
- ✅ **Recherche par tag** - Filtrage des routes par catégorie
- ✅ **Inspection des routes** - Listage de toutes les routes enregistrées
- ✅ **Métadonnées** - Informations complètes sur chaque route

```python
from microframe import Application, Router

app = Application()

# Router modulaire
users_router = Router(prefix="/users", tags=["Users"])
items_router = Router(prefix="/items", tags=["Items"])

@users_router.get("/")
async def list_users():
    return {"users": []}

@items_router.post("/")
async def create_item(name: str):
    return {"name": name}

# Inclusion dans l'app
api = Router(prefix="/api/v1")
api.include_router(users_router)
api.include_router(items_router)
app.include_router(api)
```

---

## 💉 Injection de Dépendances

### Système de Dépendances
- ✅ **Injection automatique** - Résolution automatique des dépendances
- ✅ **Cache intelligent** - Mise en cache des dépendances par requête
- ✅ **Dépendances imbriquées** - Support des dépendances de dépendances
- ✅ **Générateurs async** - Support de `async with` et cleanup
- ✅ **Type hints** - Détection automatique via annotations

### Scopes de Dépendances
- ✅ **Request scope** - Une instance par requête
- ✅ **Singleton scope** - Une instance globale
- ✅ **Factory scope** - Nouvelle instance à chaque injection

### Gestion des Erreurs
- ✅ **Exception handling** - Gestion automatique des erreurs de dépendances
- ✅ **Rollback automatique** - Cleanup en cas d'erreur
- ✅ **Traces détaillées** - Debugging facilité

```python
from microframe import Application, Depends

class Database:
    def __init__(self):
        self.connection = "connected"
    
    def query(self, sql: str):
        return f"Executing: {sql}"

def get_db():
    db = Database()
    return db

@app.get("/users")
async def list_users(db=Depends(get_db)):
    return db.query("SELECT * FROM users")
```

---

## ✅ Validation

### Validation Pydantic
- ✅ **Modèles Pydantic** - Validation automatique des données
- ✅ **Type checking** - Vérification des types à l'exécution
- ✅ **Validation personnalisée** - Validators custom
- ✅ **Messages d'erreur clairs** - Erreurs détaillées et lisibles
- ✅ **Coercition de types** - Conversion automatique des types

### Parsing de Requêtes
- ✅ **JSON body** - Parsing et validation automatique
- ✅ **Form data** - Support des formulaires HTML
- ✅ **Query parameters** - Validation des paramètres d'URL
- ✅ **Path parameters** - Validation des segments de chemin
- ✅ **Headers** - Validation des en-têtes HTTP
- ✅ **Cookies** - Lecture et validation des cookies

```python
from pydantic import BaseModel, EmailStr
from microframe import Application

class User(BaseModel):
    name: str
    email: EmailStr
    age: int

@app.post("/users")
async def create_user(user: User):
    # user est automatiquement validé
    return {"created": user.dict()}
```

---

## 🔒 Middleware et Sécurité

### Middlewares Intégrés
- ✅ **CORS Middleware** - Configuration CORS complète
- ✅ **Security Middleware** - Headers de sécurité HTTP
- ✅ **Rate Limiting** - Limitation du taux de requêtes
- ✅ **Compression** - Gzip/Brotli automatique
- ✅ **Trusted Hosts** - Validation des hôtes autorisés

### CORS (Cross-Origin Resource Sharing)
- ✅ **Origins autorisées** - Liste blanche de domaines
- ✅ **Méthodes HTTP** - Filtrage des méthodes autorisées
- ✅ **Headers personnalisés** - Configuration des headers CORS
- ✅ **Credentials** - Support des cookies cross-origin
- ✅ **Preflight requests** - Gestion des requêtes OPTIONS

### Sécurité
- ✅ **Security headers** - HSTS, X-Frame-Options, CSP, etc.
- ✅ **Rate limiting** - Protection contre les abus
- ✅ **Request validation** - Validation des requêtes entrantes
- ✅ **XSS protection** - Protection contre les attaques XSS
- ✅ **CSRF tokens** - Protection CSRF pour formulaires

```python
from microframe import Application
from microframe.middleware import CORSMiddleware, SecurityMiddleware

app = Application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_middleware(
    SecurityMiddleware,
    rate_limit_requests=100,
    rate_limit_window=60
)
```

---

## 📚 Documentation Automatique

### OpenAPI 3.0
- ✅ **Génération automatique** - Schéma OpenAPI complet
- ✅ **Descriptions** - Documentation inline des routes
- ✅ **Exemples** - Exemples de requêtes/réponses
- ✅ **Tags et catégories** - Organisation de la documentation
- ✅ **Schémas Pydantic** - Conversion automatique en JSON Schema

### Interfaces Interactives
- ✅ **Swagger UI** - Interface interactive pour tester l'API
- ✅ **ReDoc** - Documentation élégante et responsive
- ✅ **Personnalisable** - Customisation des thèmes et styles
- ✅ **URLs configurables** - Chemins personnalisables

### Métadonnées
- ✅ **Titre et version** - Informations sur l'API
- ✅ **Description** - Documentation générale
- ✅ **License** - Informations de licence
- ✅ **Contact** - Coordonnées du mainteneur
- ✅ **Servers** - URLs des serveurs (dev, staging, prod)

```python
from microframe import Application, AppConfig

app = Application(
    configuration=AppConfig(
        title="Ma Super API",
        version="1.0.0",
        description="Documentation complète de mon API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
)
```

---

## 🎨 Moteur de Templates

### Jinja2 Intégré
- ✅ **Templates Jinja2** - Moteur de templates puissant et flexible
- ✅ **Héritage de templates** - Layouts et blocks
- ✅ **Includes** - Réutilisation de fragments
- ✅ **Macros** - Fonctions réutilisables dans les templates
- ✅ **Filtres personnalisés** - Extensions du système de filtres
- ✅ **Variables globales** - Contexte partagé entre templates

### Cache de Templates
- ✅ **Compilation automatique** - Templates pré-compilés
- ✅ **Cache en mémoire** - Performance optimale
- ✅ **Hot reload** - Rechargement automatique en dev
- ✅ **Invalidation** - Gestion intelligente du cache

### Système de Composants
- ✅ **Composants réutilisables** - Système de composants UI
- ✅ **Props et slots** - Passage de données aux composants
- ✅ **Composition** - Composition de composants
- ✅ **Rendu côté serveur** - SSR pour performance maximale

```python
from microframe import Application
from microframe.engine import TemplateEngine

app = Application()
engine = TemplateEngine(templates_dir="templates")

@app.get("/")
async def index(request):
    return engine.render("index.html", {
        "title": "Accueil",
        "user": {"name": "John Doe"},
        "items": [1, 2, 3]
    })
```

---

## 🧩 Composants UI

### Bibliothèque de Composants
- ✅ **Cards** - Cartes d'information stylisées
- ✅ **Buttons** - Boutons avec différents styles
- ✅ **Forms** - Formulaires avec validation
- ✅ **Tables** - Tableaux de données
- ✅ **Modals** - Fenêtres modales
- ✅ **Alerts** - Messages d'alerte et notifications
- ✅ **Navigation** - Barres de navigation et menus

### Layouts
- ✅ **Grid system** - Système de grille responsive
- ✅ **Flex layouts** - Layouts flexbox
- ✅ **Containers** - Conteneurs et wrappers
- ✅ **Sections** - Sections de page
- ✅ **Headers/Footers** - En-têtes et pieds de page

### Formulaires
- ✅ **Input fields** - Champs de saisie variés
- ✅ **Validation côté client** - Validation HTML5
- ✅ **Validation côté serveur** - Intégration Pydantic
- ✅ **Messages d'erreur** - Affichage des erreurs de validation
- ✅ **File uploads** - Upload de fichiers avec prévisualisation

```python
from microframe.ui.components import Card, Button, Form
from microframe.ui.layouts import Container, Grid

# Création d'une card
card = Card(
    title="Dashboard",
    content="Bienvenue sur votre tableau de bord",
    actions=[
        Button("Voir plus", variant="primary"),
        Button("Annuler", variant="secondary")
    ]
)

# Layout avec grille
layout = Container([
    Grid(columns=3, items=[card, card, card])
])
```

---

## ⚙️ Configuration

### Configuration Modulaire
- ✅ **Configuration par environnement** - Dev, staging, production
- ✅ **Variables d'environnement** - Support des .env
- ✅ **Validation automatique** - Schémas Pydantic pour config
- ✅ **Hot reload** - Rechargement sans redémarrage
- ✅ **Configuration hiérarchique** - Override de configurations

### Modules de Configuration
- ✅ **Base configuration** - Configuration de base du framework
- ✅ **JWT configuration** - Paramètres d'authentification JWT
- ✅ **Security configuration** - Paramètres de sécurité
- ✅ **Middleware configuration** - Config des middlewares
- ✅ **Database configuration** - Paramètres de base de données

### Configuration Manager
- ✅ **Chargement depuis fichiers** - JSON, YAML, TOML
- ✅ **Chargement depuis env** - Variables d'environnement
- ✅ **Get/Set dynamique** - Accès programmatique
- ✅ **Validation** - Vérification automatique des valeurs
- ✅ **Secrets management** - Gestion sécurisée des secrets

```python
from microframe.configurations import ConfigManager
from microframe.configurations.base import BaseConfig

class DatabaseConfig(BaseConfig):
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    username: str
    password: str

config = ConfigManager()
config.register("database", DatabaseConfig())
config.load_from_file("config.json")

db_config = config.get("database")
print(f"Connecting to {db_config.host}:{db_config.port}")
```

---

## 🛠️ Utilitaires

### Helpers
- ✅ **String utils** - Manipulation de chaînes
- ✅ **Date utils** - Gestion des dates et timestamps
- ✅ **File utils** - Manipulation de fichiers
- ✅ **URL utils** - Parsing et construction d'URLs
- ✅ **JSON utils** - Sérialisation/désérialisation avancée

### Validateurs Personnalisés
- ✅ **Email validation** - Validation d'emails
- ✅ **URL validation** - Validation d'URLs
- ✅ **Phone validation** - Validation de numéros de téléphone
- ✅ **Password strength** - Vérification de force de mot de passe
- ✅ **Custom validators** - Créez vos propres validateurs

### Décorateurs Utilitaires
- ✅ **@cached** - Cache de fonction avec TTL
- ✅ **@retry** - Retry automatique en cas d'erreur
- ✅ **@timeout** - Timeout pour fonctions async
- ✅ **@rate_limit** - Limitation de taux par fonction
- ✅ **@log_execution** - Logging automatique

```python
from microframe.utils.decorators import cached, retry
from microframe.utils.validators import validate_email, validate_url

@cached(ttl=300)  # Cache pendant 5 minutes
@retry(max_attempts=3, delay=1)
async def fetch_user_data(user_id: int):
    # Votre logique avec cache et retry automatique
    return {"user_id": user_id, "name": "John"}

# Validation
email = "user@example.com"
if validate_email(email):
    print("Email valide!")
```

---

## 🧪 Testing

### Suite de Tests Complète
- ✅ **Tests unitaires** - Tests de tous les modules
- ✅ **Tests d'intégration** - Tests end-to-end
- ✅ **Tests de validation** - Validation des schémas
- ✅ **Tests de middleware** - Tests des middlewares
- ✅ **Tests de templates** - Tests du moteur de templates
- ✅ **Tests UI** - Tests des composants UI

### Fixtures et Helpers
- ✅ **Fixtures pytest** - Fixtures réutilisables
- ✅ **Test client** - Client HTTP pour tests
- ✅ **Mock objects** - Mocking facilité
- ✅ **Factory pattern** - Factories pour données de test
- ✅ **Assertions personnalisées** - Helpers d'assertion

### Coverage
- ✅ **Code coverage** - Mesure de la couverture
- ✅ **Rapports HTML** - Rapports de couverture détaillés
- ✅ **100+ tests** - Suite de tests exhaustive

```python
import pytest
from httpx import AsyncClient
from microframe import Application

@pytest.fixture
async def client():
    app = Application()
    
    @app.get("/test")
    async def test_route():
        return {"message": "ok"}
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_route(client):
    response = await client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
```

---

## 📊 Récapitulatif des Fonctionnalités

### Framework Core
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| ASGI 3.0 | ✅ | Supporté via Starlette |
| Async/Await | ✅ | Support complet async |
| Type Hints | ✅ | Typing moderne Python 3.13+ |
| Hot Reload | ✅ | Rechargement automatique en dev |
| Configuration | ✅ | Configuration centralisée |

### Routing & HTTP
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| HTTP Methods | ✅ | GET, POST, PUT, DELETE, PATCH, etc. |
| Route Parameters | ✅ | Paramètres dynamiques |
| Query Parameters | ✅ | Parsing automatique |
| Request Body | ✅ | JSON, Form, Multipart |
| Routers Modulaires | ✅ | Organisation hiérarchique |

### Validation & Sécurité
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| Pydantic Models | ✅ | Validation automatique |
| CORS | ✅ | Configuration CORS complète |
| Rate Limiting | ✅ | Protection contre abus |
| Security Headers | ✅ | Headers de sécurité HTTP |
| Authentication | ✅ | JWT, sessions, custom |

### Documentation
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| OpenAPI 3.0 | ✅ | Schéma auto-généré |
| Swagger UI | ✅ | Interface interactive |
| ReDoc | ✅ | Documentation élégante |
| Type Annotations | ✅ | Documentation inline |

### Templates & UI
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| Jinja2 | ✅ | Moteur de templates |
| Components | ✅ | Composants réutilisables |
| Layouts | ✅ | Système de layouts |
| Forms | ✅ | Formulaires avec validation |
| Cache | ✅ | Cache de templates |

### Avancé
| Fonctionnalité | Status | Description |
|----------------|--------|-------------|
| Dependency Injection | ✅ | Injection automatique |
| Configuration Manager | ✅ | Gestion centralisée |
| Middleware Custom | ✅ | Middlewares personnalisés |
| Testing Suite | ✅ | 100+ tests complets |
| Performance | ✅ | Cache, lazy loading |

---

## 🚀 Points Forts

### Performance
- ⚡ **ASGI natif** - Performance maximale avec async
- ⚡ **Cache intelligent** - Dépendances et templates cachés
- ⚡ **Lazy loading** - Import à la demande
- ⚡ **Registry O(1)** - Résolution de routes ultra-rapide

### Développement
- 🎯 **Type safety** - Type hints partout
- 🎯 **Auto-completion** - IDE support optimal
- 🎯 **Hot reload** - Développement rapide
- 🎯 **Debugging** - Messages d'erreur clairs

### Production
- 🔒 **Sécurité** - CORS, rate limiting, headers
- 🔒 **Scalabilité** - Architecture modulaire
- 🔒 **Monitoring** - Logs et métriques
- 🔒 **Documentation** - OpenAPI auto-générée

---

## 📦 Installation

```bash
# Installation via poetry
poetry add microframe

# Installation via pip
pip install microframe
```

## 🎓 Démarrage Rapide

```python
from microframe import Application

app = Application(title="Mon API", version="1.0.0")

@app.get("/")
async def index():
    return {"message": "Hello, MicroFrame!"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📚 Documentation

- 📖 [Architecture](ARCHITECTURE.md) - Architecture détaillée du framework
- 📖 [Migration Guide](MIGRATION_GUIDE.md) - Guide de migration v1 → v2
- 📖 [Refactoring Summary](REFACTORING_SUMMARY.md) - Résumé des changements
- 📖 [Examples](../examples/) - Exemples d'applications complètes

---

**Version**: 2.0.0  
**Python**: 3.13+  
**License**: MIT  
**Repository**: [traoreera/microframe](https://github.com/traoreera/microframe)
