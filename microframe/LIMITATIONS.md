# MicroFrame v2.0 - Limitations et Points d'Amélioration

> Documentation des limitations actuelles, bugs connus et zones d'amélioration du framework

**Version**: 2.0.0  
**Date de mise à jour**: 2025-11-23  
**Status**: Document vivant - mis à jour régulièrement

---

## 📋 Table des matières

- [Limitations Architecturales](#-limitations-architecturales)
- [Fonctionnalités Manquantes](#-fonctionnalités-manquantes)
- [Problèmes de Performance](#-problèmes-de-performance)
- [Bugs Connus](#-bugs-connus)
- [Documentation Incomplète](#-documentation-incomplète)
- [Scalabilité](#-scalabilité)
- [Sécurité](#-sécurité)
- [DX (Developer Experience)](#-dx-developer-experience)
- [Tests](#-tests)
- [Roadmap](#-roadmap)

---

## ⚠️ Limitations Architecturales

### 1. **Système Depends Dupliqu** (AuthX vs Core)
**Sévérité**: 🟡 Moyen

**Problème**:
- `authx/dependencies.py` a son propre système `Depends`
- `microframe/dependencies/` a un autre système `Depends`
- Les deux ne sont PAS compatibles entre eux
- Peut créer confusion pour utilisateurs

**Impact**:
```python
# ❌ Confusion possible
from microframe import Depends  # Un système
from microframe.authx import Depends  # Un autre système !

# Ces deux Depends ne fonctionnent pas ensemble
```

**Note**: AuthX est un **module optionnel séparé installable indépendamment** pour faciliter la maintenabilité. Cette séparation est intentionnelle.

**Solution future**: Faire que `authx.Depends` utilise `microframe.Depends` en interne

---

### 2. **État en Mémoire Non Distribué**
**Sévérité**: 🔴 Critique pour production multi-instance

**Problème**:
- Le cache des dépendances est stocké en mémoire locale
- Pas de cache partagé entre instances multiples
- Sessions non distribuées

**Impact**:
```python
# ❌ Cache local uniquement
self._dependency_manager = DependencyManager()
# Cache non partagé entre instances
```

**Contournement**:
- Utiliser Redis/Memcached pour cache distribué
- Implémenter sticky sessions au load balancer
- Utiliser external state store (Redis, PostgreSQL)

**Solution future**: Intégration Redis native

---

### 3. **Pas de Support WebSocket Documenté**
**Sévérité**: 🟡 Moyen

**Problème**:
- WebSockets supportés par Starlette mais non documentés
- Pas d'exemples d'implémentation
- Injection de dépendances non testée avec WS

**Impact**:
- Développeurs doivent implémenter eux-mêmes
- Pas de best practices

**Solution future**: Documentation + exemples WebSocket

---

### 4. **Injection de Dépendances Limitée**
**Sévérité**: 🟡 Moyen

**Problème**:
- Pas de scopes configurables (singleton, transient, scoped)
- Cache par requête uniquement
- Pas de lifecycle hooks (OnInit, OnDestroy)

**Code actuel**:
```python
# Scope fixé à "request" seulement
def dependency(self, name: str = "", cache: bool = False, 
               scope: Literal["app", "request"] = "request"):
    # Scope "app" non implémenté
```

**Solution future**: Système de scopes complet

---

### 5. **Pas de Gestion d'Événements**
**Sévérité**: 🟢 Faible

**Problème**:
- Pas de système d'événements/hooks
- Pas de middleware hooks avancés
- Pas de plugin system

**Fonctionnalités manquantes**:
- `before_request`, `after_request` hooks
- Event bus pour communication inter-composants
- Plugin architecture

---

## 🚫 Fonctionnalités Manquantes

### 1. **ORM / Database Layer**
**Sévérité**: 🟡 Moyen

**Manquant**:
- ❌ Pas d'ORM intégré (SQLAlchemy, Tortoise)
- ❌ Pas de migrations database
- ❌ Pas de connection pooling natif
- ❌ Pas d'exemples async database

**Recommandation actuelle**:
```python
# Utilisateurs doivent implémenter manuellement
from databases import Database
db = Database("postgresql://...")
```

---

### 2. **Module AuthX - Intégration Incomplète**
**Sévérité**: 🟡 Moyen (module existe mais non intégré)

**État actuel**:
- ✅ Module `authx/` existe avec JWT complet
- ✅ Helpers JWT: `create_access_token`, `create_refresh_token`, `decode_token`
- ✅ Password hashing: `hash_password`, `verify_password`
- ✅ AuthManager abstrait pour extensibilité
- ✅ Modèles Pydantic: `UserResponse`, `TokenResponse`, `LoginRequest`
- ✅ Exceptions: `AuthException`, `CredentialsException`, `InvalidTokenException`

**Limitations**:
- ⚠️ **Non intégré avec Application** - Pas dans `microframe/__init__.py`
- ⚠️ **Pas de routes par défaut** - Utilisateurs doivent créer routes manuellement
- ⚠️ **Pas de middleware auth** - Pas de protection automatique des routes
- ⚠️ **Documentation séparée** - Pas dans docs principales
- ❌ **Pas de RBAC** - Pas de système de rôles/permissions
- ❌ **Pas d'OAuth2 flow** - Seulement JWT basique
- ❌ **Pas de session management** - Stateless uniquement
- ❌ **Pas de refresh token rotation** - Pas de blacklist

**Impact**:
```python
# ❌ Impossible actuellement (pas exporté)
from microframe import AuthManager, create_access_token

# ✅ Workaround (import direct)
from microframe.authx import AuthManager, create_access_token

# ❌ Pas de protection automatique
@app.get("/protected")  # N'importe qui peut accéder
async def protected():
    return {"data": "secret"}

# ✅ Doit implémenter manuellement
from microframe.authx import get_current_user, Depends
@app.get("/protected")
async def protected(user = Depends(get_current_user)):
    # Mais Depends n'est pas le Depends de microframe !
    return {"user": user}
```

**Fichiers AuthX existants**:
- `authx/__init__.py` (202 lignes) - Exports et docs
- `authx/config.py` - Configuration AuthConfig
- `authx/jwt.py` - Création/validation tokens
- `authx/manager.py` - AuthManager abstrait
- `authx/models.py` - Modèles Pydantic
- `authx/security.py` - Hash passwords (bcrypt)
- `authx/exceptions.py` - Exceptions custom
- `authx/dependencies.py` - Système Depends (séparé!)
- `authx/README.md` (374 lignes) - Documentation complète

**Solutions nécessaires**:
1. Intégrer authx dans `microframe/__init__.py`
2. Créer `create_auth_routes()` helper
3. Middleware de protection automatique
4. Unifier système Depends avec core
5. Ajouter RBAC et permissions

---

### 3. **Validation Avancée**
**Sévérité**: 🟡 Moyen

**Limitations**:
- ❌ Pas de validation de headers customisée
- ❌ Pas de validation de cookies
- ❌ Pas de validation de files uploads
- ❌ Pas de custom error messages globaux

**Code actuel**:
```python
# Validation limitée au body et query params
async def parse(self, request: Request, func: Callable):
    # Headers validation manquante
    # File validation manquante
```

---

### 4. **Monitoring et Observabilité**
**Sévérité**: 🔴 Critique pour production

**Manquant**:
- ❌ Pas de métriques Prometheus
- ❌ Pas de tracing distribué (OpenTelemetry)
- ❌ Pas de health checks standardisés
- ❌ Pas de structured logging
- ❌ Pas d'APM (Application Performance Monitoring)

**Besoin**:
```python
# Métriques souhaitées
- Request count
- Response time (p50, p95, p99)
- Error rate
- Active connections
```

---

### 5. **Background Tasks**
**Sévérité**: 🟡 Moyen

**Manquant**:
- ❌ Pas de support background tasks natif
- ❌ Pas de job queue (Celery, RQ)
- ❌ Pas de scheduled tasks (cron)

**Contournement**: Utiliser Celery/RQ séparément

---

### 6. **File Uploads Avancés**
**Sévérité**: 🟡 Moyen

**Limitations**:
- ❌ Pas de streaming upload pour gros fichiers
- ❌ Pas d'intégration S3/cloud storage
- ❌ Pas de compression automatique
- ❌ Pas de validation de type MIME

---

### 7. **GraphQL Support**
**Sévérité**: 🟢 Faible

**Manquant**:
- ❌ Pas de support GraphQL
- ❌ Pas d'intégration Strawberry/Graphene

---

## 🐌 Problèmes de Performance

### 1. **Moteur de Templates Non Optimisé pour Production**
**Sévérité**: 🟡 Moyen

**Problème**:
```python
# engine/engine.py
enable_async=True,  # OK
# Mais pas de:
# - Compiled templates persistence
# - Template preloading
# - Bytecode cache
```

**Impact**: Recompilation à chaque redémarrage

---

### 2. **Pas de Response Caching**
**Sévérité**: 🟡 Moyen

**Manquant**:
- ❌ Pas de HTTP caching headers automatiques
- ❌ Pas de response caching middleware
- ❌ Pas d'ETag generation

---

### 3. **Validation Pydantic Performance**
**Sévérité**: 🟢 Faible

**Problème**:
- Validation répétée même pour données identiques
- Pas de validation result caching

---

## 🐛 Bugs Connus

### 1. **AuthX Depends Confusion**
**Sévérité**: 🟡 Moyen  
**Fichier**: `authx/dependencies.py`

**Problème**:
```python
# authx a son propre système Depends
from authx.dependencies import Depends, resolve_dependencies

# Incompatible avec microframe.Depends
from microframe import Depends 

# Utilisateurs confus sur lequel utiliser
```

**Impact**: Incompatibilité entre authx et routes normales

**Fix suggéré**: Utiliser le Depends de microframe dans authx

---

### 2. **AuthX JWT Decode Double Exception**
**Sévérité**: 🟢 Faible  
**Fichier**: `authx/jwt.py:52-53`

**Problème**:
```python
def decode_token(token: str, config: AuthConfig, expected_type: str):
    try:
        # ...
    except JWTError:
        raise TokenExpiredException()
    except JWTError:  # ❌ Jamais atteint (duplicate)
        raise InvalidTokenException()
```

**Impact**: `InvalidTokenException` jamais levée

---

### 3. **Rate Limiting Lock Contention**
**Sévérité**: 🟡 Moyen  
**Fichier**: `middleware/security_middleware.py:26`

**Problème**:
```python
self.lock = asyncio.Lock()  # Lock global
# Peut créer bottleneck sous haute charge
```

**Impact**: Performance dégradée avec forte concurrence

**Fix suggéré**: Lock per-client au lieu de global

---

### 4. **Exception Handling Generic**
**Sévérité**: 🟡 Moyen  
**Fichier**: `core/application.py:252`

**Problème**:
```python
async def _generic_exception_handler(self, request: Request, exc: Exception):
    self.logger.error(f"Erreur non gérée: {exc}", exc_info=True)
    return JSONResponse({"error": "Internal server error"}, status_code=500)
    # Pas de détails en dev mode
    # Pas de error ID pour tracking
```

**Impact**: Debugging difficile en production

---

### 5. **Tests Hanging**
**Sévérité**: 🔴 Critique  
**Observé**: 2025-11-23

**Problème**:
```bash
poetry run pytest -v
# Tests ne se terminent jamais
# Pas d'output
```

**Cause probable**:
- Import circulaire
- Fixture non terminée
- Async cleanup manquant

**Status**: Investigation en cours

---

### 6. **Dependency Injection Error Messages**
**Sévérité**: 🟡 Moyen  
**Fichier**: `dependencies/exceptionHandler.py`

**Problème**:
```python
# Messages d'erreur peu clairs
except Exception as e:
    raise ValueError(f"Failed to resolve dependency")
    # Pas de stack trace de la dépendance
```

---

## 📚 Documentation Incomplète

### 1. **Exemples Manquants**

**Manquant**:
- ❌ Exemples database (PostgreSQL, MongoDB)
- ❌ Exemples authentication complète
- ❌ Exemples microservices
- ❌ Exemples deployment (Docker, K8s)
- ❌ Exemples testing avancés
- ❌ Exemples WebSocket
- ❌ Exemples background tasks

---

### 2. **Documentation API Incomplète**

**Modules sans docstrings complètes**:
- `configurations/` - 60% documenté
- `ui/` - 40% documenté
- `utils/` - 30% documenté

---

### 3. **Guides Manquants**

**Guides nécessaires**:
- ❌ Production deployment guide
- ❌ Performance tuning guide
- ❌ Security best practices
- ❌ Testing strategy guide
- ❌ Troubleshooting guide
- ❌ Contributing guide détaillé

---

## 📊 Scalabilité

### 1. **Pas de Métriques de Scalabilité**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Benchmarks officiels
- Load testing results
- Comparaison avec autres frameworks
- Scalability limits documentés

---

### 2. **Configuration Production Non Documentée**
**Sévérité**: 🟡 Moyen

**Manquant**:
```python
# Configuration optimale pour prod ?
# - Nombre de workers ?
# - Taille du cache ?
# - Timeouts recommandés ?
# - Resource limits ?
```

---

### 3. **Pas de Circuit Breaker**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Pattern circuit breaker pour services externes
- Retry policy configurable
- Timeout handling avancé

---

## 🔒 Sécurité

### 1. **Pas de Security Audit**
**Sévérité**: 🔴 Critique

**Problème**:
- Aucun audit de sécurité professionnel
- Pas de scan de vulnérabilités automatique
- Pas de security policy documentée

---

### 2. **CSRF Protection Manquante**
**Sévérité**: 🔴 Critique

**Problème**:
```python
# middleware/security.py mentionne CSRF
# Mais implémentation incomplète
# Pas de CSRF tokens pour forms
```

---

### 3. **Input Sanitization Limitée**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Sanitization HTML automatique
- SQL injection protection docs
- XSS protection examples

---

### 4. **Secrets Management**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Pas d'intégration vault (HashiCorp, AWS Secrets)
- Pas de rotation de secrets
- Pas de best practices documentées

---

### 5. **Rate Limiting Basique**
**Sévérité**: 🟡 Moyen

**Limitations**:
```python
# Rate limiting par IP uniquement
# Pas de rate limiting par user
# Pas de rate limiting par endpoint
# Pas de distributed rate limiting (Redis)
```

---

## 👨‍💻 DX (Developer Experience)

### 1. **Messages d'Erreur Peu Clairs**
**Sévérité**: 🟡 Moyen

**Exemples**:
```python
# Erreurs génériques
"Failed to resolve dependency"
"Validation error"
"Internal server error"

# Pas de suggestions
# Pas de liens vers docs
```

---

### 2. **CLI Tools Manquants**
**Sévérité**: 🟡 Moyen

**Manquant**:
- ❌ CLI pour générer routes
- ❌ CLI pour générer models
- ❌ CLI pour migrations
- ❌ CLI pour scaffolding

**Souhaité**:
```bash
microframe init my-project
microframe generate route users
microframe generate model User
```

---

### 3. **IDE Support Limité**
**Sévérité**: 🟢 Faible

**Problème**:
- Pas de plugin VSCode
- Pas de snippets officiels
- Type hints incomplets dans certains modules

---

### 4. **Hot Reload Incomplet**
**Sévérité**: 🟡 Moyen

**Problème**:
- Hot reload fonctionne pour code
- Mais pas pour:
  - Templates changes
  - Configuration changes
  - Static files

---

## 🧪 Tests

### 1. **Coverage Incomplet**
**Sévérité**: 🟡 Moyen

**Stats actuels**:
- `core/` - ~70% coverage
- `routing/` - ~60% coverage
- `middleware/` - ~50% coverage
- `ui/` - ~30% coverage ❌
- `configurations/` - ~20% coverage ❌
- `utils/` - ~40% coverage

**Objectif**: 80%+ partout

---

### 2. **Tests d'Intégration Limités**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Tests multi-routers
- Tests avec database réelle
- Tests avec Redis
- Tests de performance
- Tests de charge

---

### 3. **Tests Asynchrones Instables**
**Sévérité**: 🔴 Critique

**Problème**:
- Tests hanging (cf. bugs connus)
- Fixtures async mal configurées
- Cleanup incomplet

---

### 4. **Pas de Tests End-to-End**
**Sévérité**: 🟡 Moyen

**Manquant**:
- Tests navigateur (Playwright/Selenium)
- Tests d'API complètes
- Tests de scénarios utilisateur

---

## 📦 Dépendances et Compatibilité

### 1. **Python Version Restrictive**
**Sévérité**: 🟡 Moyen

**Problème**:
```toml
python = ">=3.13"  # Très récent
```

**Impact**:
- Exclut Python 3.9, 3.10, 3.11, 3.12
- Limite adoption
- Dépendances peuvent ne pas supporter 3.13

**Recommandation**: Support Python 3.9+

---

### 2. **Dépendances Non Verrouillées**
**Sévérité**: 🟡 Moyen

**Problème**:
```toml
starlette = "^0.37.2"  # ^ permet updates
# Risque de breaking changes
```

---

### 3. **Dépendances Lourdes**
**Sévérité**: 🟢 Faible

**Installation complète**:
- 20+ dépendances directes
- 50+ dépendances transitives
- ~200MB installé

---

## 🎯 Priorités d'Amélioration

### **P0 - Critique** (À faire immédiatement)

1. ✅ Fixer tests hanging
2. ✅ Ajouter authentication/authorization
3. ✅ Security audit
4. ✅ Documentation deployment production
5. ✅ Support Python 3.9+

### **P1 - Important** (3 mois)

1. ✅ Métriques et monitoring
2. ✅ Cache distribué (Redis)
3. ✅ WebSocket documentation
4. ✅ Exemples database
5. ✅ CLI tools

### **P2 - Nice to have** (6 mois)

1. ✅ ORM intégration
2. ✅ GraphQL support
3. ✅ Background tasks
4. ✅ Plugin system
5. ✅ IDE plugins

---

## 📈 Roadmap

### **v2.1.0** (Q1 2025)
- 🔧 Fix critical bugs (tests, rate limiting)
- 🔒 Authentication système complet
- 📊 Monitoring basique (Prometheus)
- 📚 Documentation améliorée
- 🐍 Python 3.9+ support

### **v2.2.0** (Q2 2025)
- 🗄️ ORM intégration (SQLAlchemy)
- 🔌 WebSocket complet
- ⚡ Cache distribué Redis
- 🧪 Coverage 80%+
- 🛠️ CLI tools

### **v3.0.0** (Q3-Q4 2025)
- 🎨 Plugin architecture
- 📡 GraphQL support
- 🔄 Background tasks
- 🌍 i18n support
- 🚀 Performance optimizations

---

## 🤝 Comment Contribuer

Ces limitations sont des **opportunités de contribution** !

### **Comment aider**:

1. **Reporter un bug**: Ouvrir une issue sur GitHub
2. **Proposer une amélioration**: Issue avec label `enhancement`
3. **Contribuer du code**: Pull request avec tests
4. **Améliorer la doc**: PR sur fichiers .md
5. **Partager des exemples**: Examples/ directory

### **Guidelines**:
- Toute PR doit avoir des tests
- Maintenir coverage > 70%
- Suivre style guide (Black, flake8)
- Documenter avec docstrings

---

## 📝 Notes de Version

### **Limitations connues v2.0.0**:
- Tests suite incomplete et instable
- Authentification non implémentée
- Monitoring absent
- Documentation d'exemples limitée
- Python 3.13 uniquement

**Transparence**: Ce document est maintenu par l'équipe pour être transparent sur les limitations actuelles et guider les améliorations futures.

---

## 📞 Contact et Support

- **Issues**: [GitHub Issues](https://github.com/traoreera/microframe/issues)
- **Discussions**: [GitHub Discussions](https://github.com/traoreera/microframe/discussions)
- **Email**: traoreera@gmail.com

---

**Dernière mise à jour**: 2025-11-23  
**Mainteneur**: @traoreera  
**Status**: Document actif - contributions bienvenues
