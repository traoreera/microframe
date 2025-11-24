# 🚀 MicroFrame v2.0 - Roadmap

> Roadmap de développement et corrections pour MicroFrame v2.0+

**Version actuelle** : 2.0.0  
**Dernière mise à jour** : 2025-11-24  
**Mainteneur** : [@traoreera](https://github.com/traoreera)

---

## 📊 Vue d'ensemble

| Version | Date cible | Focus | Status |
|---------|-----------|-------|--------|
| **v2.0.1** | Q1 2025 | Bugs critiques | 🔴 En cours |
| **v2.1.0** | Q1 2025 | Stabilité + Docs | 🟡 Planifié |
| **v2.2.0** | Q2 2025 | Features avancées | 🟢 Backlog |
| **v3.0.0** | Q3-Q4 2025 | Architecture majeure | ⚪ Concept |

---

## 🔥 v2.0.1 - Correctifs Critiques (Immédiat)

> **Date cible** : Janvier 2025  
> **Focus** : Fixer les bugs bloquants

### 🐛 Bugs Critiques à Fixer

#### 1. **Tests Hanging** 🔴 P0
**Fichier** : `tests/`  
**Problème** : Tests ne se terminent jamais avec pytest  
**Impact** : Bloque le développement et CI/CD

**Actions** :
- [ ] Investiguer imports circulaires
- [ ] Vérifier fixtures async mal configurées
- [ ] Ajouter cleanup async manquant
- [ ] Tester avec `pytest -v -s` pour debug
- [ ] Isoler tests problématiques

**Estimation** : 2-3 jours

---

#### 2. **AuthX JWT Decode Double Exception** 🟢 P2
**Fichier** : `authx/jwt.py:52-53`  
**Problème** : Code mort - deuxième `except JWTError` jamais atteint

```python
# AVANT (bugné)
try:
    payload = jwt.decode(...)
except JWTError:
    raise TokenExpiredException()
except JWTError:  # ❌ Jamais atteint !
    raise InvalidTokenException()

# APRÈS (corrigé)
try:
    payload = jwt.decode(...)
except ExpiredSignatureError:
    raise TokenExpiredException()
except JWTError:
    raise InvalidTokenException()
```

**Actions** :
- [ ] Différencier exceptions JWT
- [ ] Tester avec token expiré
- [ ] Tester avec token invalide
- [ ] Mettre à jour tests

**Estimation** : 1 jour

---

#### 3. **AuthX Depends Incompatibilité** 🟡 P1
**Fichiers** : `authx/dependencies.py` vs `microframe/dependencies/`  
**Problème** : Deux systèmes Depends incompatibles

**Actions** :
- [ ] Unifier AuthX pour utiliser `microframe.Depends`
- [ ] Supprimer `authx/dependencies.py` ou l'adapter
- [ ] Mettre à jour imports dans `authx/`
- [ ] Tests d'intégration authx + microframe
- [ ] Documenter dans migration guide

**Estimation** : 3-4 jours

---

#### 4. **Rate Limiting Lock Contention** 🟡 P1
**Fichier** : `middleware/security_middleware.py:26`  
**Problème** : Lock global → bottleneck haute charge

```python
# AVANT (bottleneck)
self.lock = asyncio.Lock()  # Global lock

# APRÈS (optimisé)
self.locks: Dict[str, asyncio.Lock] = {}  # Lock per client
```

**Actions** :
- [ ] Implémenter lock per-client-IP
- [ ] Benchmarker performance
- [ ] Tests de charge (100+ req/s)
- [ ] Documentation performance

**Estimation** : 2 jours

---

### 📚 Documentation Urgente

#### 5. **Compléter Documentation** 🟡 P1

**Actions** :
- [x] Index principal (`docs/README.md`) ✅
- [x] Getting Started (`docs/guides/getting-started.md`) ✅
- [ ] Authentication guide (`docs/guides/authentication.md`)
- [ ] WebSocket guide (`docs/guides/websocket-chat.md`)
- [ ] Deployment guide (`docs/guides/deployment.md`)
- [ ] Best practices (`docs/guides/best-practices.md`)
- [ ] Templates docs (`docs/microframe/templates.md`)
- [ ] Configurations docs (`docs/microframe/configurations.md`)

**Estimation** : 1 semaine

---

## 🎯 v2.1.0 - Stabilité et Améliorations (Q1 2025)

> **Date cible** : Mars 2025  
> **Focus** : Stabilisation, tests, documentation complète

### ✅ Tests et Qualité

#### 1. **Coverage 80%+ Partout** 🟡
**Modules à améliorer** :
- [ ] `authx/` - Ajouter tests (actuellement 0%)
- [ ] `ws/` - Tests WebSocket (actuellement 0%)
- [ ] `ui/` - De 30% → 80%
- [ ] `configurations/` - De 20% → 80%
- [ ] `utils/` - De 40% → 80%

**Actions** :
- [ ] Tests unitaires pour tous modules
- [ ] Tests d'intégration authx + app
- [ ] Tests WebSocket avec clients multiples
- [ ] Tests de charge (benchmark)

**Estimation** : 2 semaines

---

#### 2. **Tests End-to-End** 🟢
**Actions** :
- [ ] Playwright/Selenium pour UI tests
- [ ] Tests de scénarios complets
- [ ] Tests multi-navigateurs
- [ ] CI/CD pipeline complet

**Estimation** : 1 semaine

---

### 🔒 Sécurité

#### 3. **Security Audit** 🔴 P0
**Actions** :
- [ ] Audit professionnel (si budget)
- [ ] Scan vulnérabilités automatique (Snyk, Safety)
- [ ] Security policy documented
- [ ] OWASP checklist
- [ ] Dependency security updates

**Estimation** : 1 semaine

---

#### 4. **CSRF Protection Complète** 🔴 P0
**Fichier** : `middleware/security.py`  
**Actions** :
- [ ] Implémenter CSRF tokens pour forms
- [ ] Double-submit cookie pattern
- [ ] Tests CSRF protection
- [ ] Documentation

**Estimation** : 3-4 jours

---

### 🚀 Améliorations Performance

#### 5. **Response Caching** 🟡
**Actions** :
- [ ] HTTP caching headers automatiques
- [ ] Response caching middleware
- [ ] ETag generation
- [ ] Cache-Control directives

**Estimation** : 1 semaine

---

#### 6. **Template Bytecode Cache** 🟡
**Fichier** : `engine/engine.py`  
**Actions** :
- [ ] Persistence compiled templates
- [ ] Template preloading
- [ ] Bytecode cache optimisé

**Estimation** : 2-3 jours

---

### 📦 Compatibilité

#### 7. **Support Python 3.9+** 🟡 P1
**Problème** : Actuellement Python 3.13+ uniquement

**Actions** :
- [ ] Tester avec Python 3.9, 3.10, 3.11, 3.12
- [ ] Ajuster `pyproject.toml`
- [ ] CI pour toutes versions
- [ ] Documenter compatibilité

**Estimation** : 1 semaine

---

## 🎨 v2.2.0 - Features Avancées (Q2 2025)

> **Date cible** : Juin 2025  
> **Focus** : Nouvelles fonctionnalités

### 🗄️ Database Layer

#### 1. **ORM Intégration** 🟡
**Actions** :
- [ ] Support SQLAlchemy 2.0
- [ ] Support Tortoise ORM (optionnel)
- [ ] Migrations (Alembic)
- [ ] Connection pooling
- [ ] Examples async database

**Estimation** : 2-3 semaines

---

### 🔐 AuthX Améliorations

#### 2. **RBAC (Role-Based Access Control)** 🟡
**Actions** :
- [ ] Permission system
- [ ] Role definitions
- [ ] Decorators `@require_role()`, `@require_permission()`
- [ ] Admin panel (optionnel)

**Estimation** : 2 semaines

---

#### 3. **OAuth2 Flows** 🟢
**Actions** :
- [ ] Authorization Code flow
- [ ] Client Credentials flow
- [ ] Intégration sociale (Google, GitHub)
- [ ] Refresh token rotation
- [ ] Token blacklist

**Estimation** : 2 semaines

---

#### 4. **2FA/MFA Support** 🟢
**Actions** :
- [ ] TOTP (Time-based OTP)
- [ ] SMS verification (optionnel)
- [ ] Email verification
- [ ] Backup codes

**Estimation** : 1 semaine

---

### 🌐 WebSocket Améliorations

#### 5. **Advanced WebSocket Features** 🟢
**Actions** :
- [ ] Reconnexion automatique
- [ ] Heartbeat/ping-pong
- [ ] Compression (permessage-deflate)
- [ ] Binary messages support
- [ ] Broadcast optimizations

**Estimation** : 1 semaine

---

### 📊 Monitoring

#### 6. **Metrics et Observabilité** 🟡 P1
**Actions** :
- [ ] Prometheus metrics
- [ ] OpenTelemetry tracing
- [ ] Health checks standardisés
- [ ] Structured logging
- [ ] APM ready (New Relic, DataDog)

**Estimation** : 2 semaines

---

### 🛠️ CLI Tools

#### 7. **Command Line Interface** 🟡
**Actions** :
```bash
microframe init my-project
microframe generate route users
microframe generate model User
microframe db migrate
microframe run --reload
```

**Estimation** : 2 semaines

---

### ⚡ Cache Distribué

#### 8. **Redis Integration** 🟡 P1
**Actions** :
- [ ] Cache distribué pour dépendances
- [ ] Session storage Redis
- [ ] Rate limiting distribué
- [ ] Pub/Sub pour WebSocket scaling

**Estimation** : 1 semaine

---

## 🚀 v3.0.0 - Architecture Majeure (Q3-Q4 2025)

> **Date cible** : Septembre-Décembre 2025  
> **Focus** : Breaking changes, architecture moderne

### 🎨 Plugin Architecture

#### 1. **System de Plugins** 🟢
**Actions** :
- [ ] Plugin API
- [ ] Hook system avancé
- [ ] Plugin marketplace (optionnel)
- [ ] Plugin discovery

**Estimation** : 1 mois

---

### 📡 GraphQL Support

#### 2. **GraphQL Integration** 🟢
**Actions** :
- [ ] Strawberry integration
- [ ] Schema auto-generation
- [ ] GraphQL playground
- [ ] Subscriptions (WebSocket)

**Estimation** : 3 semaines

---

### 🔄 Background Tasks

#### 3. **Job Queue System** 🟡
**Actions** :
- [ ] Native background tasks
- [ ] Celery integration
- [ ] Scheduled tasks (cron)
- [ ] Task monitoring

**Estimation** : 2 semaines

---

### 🌍 Internationalization

#### 4. **i18n Support** 🟢
**Actions** :
- [ ] Multi-language support
- [ ] Translation helpers
- [ ] Locale detection
- [ ] Pluralization

**Estimation** : 1 semaine

---

### 🔥 Performance Optimizations

#### 5. **Advanced Optimizations** 🟢
**Actions** :
- [ ] HTTP/2 support
- [ ] Server-sent events (SSE)
- [ ] Streaming responses optimized
- [ ] Zero-copy file serving

**Estimation** : 2 semaines

---

## 📈 Métriques de Succès

### v2.0.1 (Immédiat)
- ✅ Tests ne hang plus
- ✅ 0 bugs critiques restants
- ✅ Documentation complète (80%+)

### v2.1.0 (Q1 2025)
- ✅ Coverage 80%+ tous modules
- ✅ Security audit passé
- ✅ Python 3.9+ support
- ✅ CSRF protection complète

### v2.2.0 (Q2 2025)
- ✅ ORM intégré
- ✅ RBAC fonctionnel
- ✅ Monitoring Prometheus
- ✅ CLI tools complet

### v3.0.0 (Q3-Q4 2025)
- ✅ Plugin system
- ✅ GraphQL support
- ✅ Background tasks
- ✅ i18n support

---

## 🤝 Comment Contribuer

### Bugs Critiques (v2.0.1)
1. Fork le repo
2. Créer branche `fix/bug-name`
3. Fixer avec tests
4. Pull request avec description

### Nouvelles Features
1. Ouvrir issue "Feature Request"
2. Discussion de design
3. Approbation mainteneur
4. Implementation avec tests
5. Documentation
6. Pull request

### Priorités Contribution

**Urgent (besoin aide)** :
- 🔴 Fixer tests hanging
- 🔴 Security audit
- 🟡 Compléter documentation
- 🟡 Tests coverage

**Bienvenue** :
- 🟢 Exemples d'applications
- 🟢 Traductions documentation
- 🟢 Benchmarks performance

---

## 📞 Contact

- **Issues** : [GitHub Issues](https://github.com/traoreera/microframe/issues)
- **Discussions** : [GitHub Discussions](https://github.com/traoreera/microframe/discussions)
- **Email** : traoreera@gmail.com

---

## 📝 Notes de Version

### v2.0.0 (Actuel - 2025-11-23)
- ✅ Architecture modulaire complète
- ✅ AuthX module séparé
- ✅ WebSocket avec auth JWT
- ✅ Templates Jinja2
- ✅ UI Components
- ⚠️ Tests hanging (en cours fix)
- ⚠️ Documentation partielle

---

**Dernière mise à jour** : 2025-11-24  
**Mainteneur** : @traoreera  
**License** : MIT
