# 📚 MicroFrame Documentation

> Documentation complète du framework MicroFrame v2.0 - Framework ASGI moderne et modulaire pour Python 3.13+

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/traoreera/microframe)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Démarrage Rapide

**Nouveau sur MicroFrame ?** Commencez ici :

1. **[Guide de Démarrage](guides/getting-started.md)** - Installation et première application
2. **[Exemples](../examples/)** - Applications complètes prêtes à l'emploi
3. **[Architecture](../microframe/ARCHITECTURE.md)** - Principes et design du framework

---

## 📖 Table des Matières

### 🎓 Guides Pratiques

Des tutoriels étape par étape pour maîtriser MicroFrame :

| Guide | Description | Niveau |
|-------|-------------|--------|
| **[Getting Started](guides/getting-started.md)** | Installation, première app, concepts de base | 🟢 Débutant |
| **[Authentication](guides/authentication.md)** | AuthX JWT, login, routes protégées | 🟡 Intermédiaire |
| **[WebSocket Chat](guides/websocket-chat.md)** | Temps réel, rooms, broadcasting | 🟡 Intermédiaire |
| **[Deployment](guides/deployment.md)** | Production, Docker, Nginx | 🔴 Avancé |
| **[Best Practices](guides/best-practices.md)** | Patterns, sécurité, performance | 🔴 Avancé |

---

### 🧩 Documentation des Modules

#### Core Framework
Documentation du framework principal MicroFrame :

- **[📦 Overview](microframe/README.md)** - Vue d'ensemble des modules
- **[🚀 Application](microframe/application.md)** - Classe Application et lifecycle
- **[⚙️ Configuration](microframe/config.md)** - AppConfig et paramètres
- **[🛣️ Router](microframe/router.md)** - Routing et décorateurs
- **[💉 Dependencies](microframe/dependencies.md)** - Injection de dépendances
- **[✅ Validation](microframe/validation.md)** - RequestParser et Pydantic
- **[🔒 Middleware](microframe/middleware.md)** - CORS, Security, Rate Limiting
- **[⚠️ Exceptions](microframe/exceptions.md)** - Gestion d'erreurs
- **[🎨 Templates](microframe/templates.md)** - Moteur de templates Jinja2
- **[🖼️ UI Components](microframe/ui.md)** - Système de composants UI
- **[🔧 Configurations](microframe/configurations.md)** - Configuration modulaire

#### AuthX - Authentification (Module Optionnel)
Module séparé pour authentification JWT :

- **[📦 Overview AuthX](authx/intro.md)** - Introduction au module AuthX
- **[⚙️ Configuration](authx/config.md)** - AuthConfig et paramètres JWT
- **[🔐 JWT Tokens](authx/jwt.md)** - Création et validation tokens
- **[👤 Auth Manager](authx/manager.md)** - AuthManager abstrait
- **[📋 Models](authx/model.md)** - UserResponse, TokenResponse, LoginRequest
- **[⚠️ Exceptions](authx/exceptions.md)** - AuthException, CredentialsException
- **[💉 Dependencies](authx/dependencies.md)** - get_current_user, Depends
- **[🔒 Security](authx/security.md)** - Password hashing (bcrypt)
- **[📜 License](authx/LICENSE.md)** - Licence MIT

**Installation** : `pip install microframe-authx` (module séparé)

#### WebSocket - Temps Réel (Module Intégré)
Module intégré pour WebSocket avec authentification :

- **[🌐 WebSocket Manager](ws/websocket.md)** - BaseWebSocket, ChatBase, authentification JWT

#### MicroUI - Composants UI (Module Intégré)
Bibliothèque complète de composants UI pour applications web :

- **[📦 Overview MicroUI](microui/README.md)** - Introduction et vue d'ensemble
- **[🎨 DaisyUI Kit](microui/daisy_ui_kit.md)** - Composants basés sur DaisyUI
- **[🚀 Advanced](microui/advance.md)** - Composants avancés
- **[📄 Pages](microui/pages.md)** - Templates de pages complètes
- **[📐 Layout](microui/layout.md)** - Layouts et structure de page
- **[📱 Layout Pages](microui/layout_pages.md)** - Pages avec layouts prédéfinis
- **[🎨 Themes](microui/thems.md)** - Système de thèmes et personnalisation
- **[🔧 Utils](microui/utils.md)** - Utilitaires et helpers UI

---

### 📚 Documentation Complémentaire

- **[🏗️ Architecture](../microframe/ARCHITECTURE.md)** - Architecture détaillée du framework
- **[🔄 Migration Guide](../microframe/MIGRATION_GUIDE.md)** - Migration v1 → v2
- **[📝 Refactoring Summary](../microframe/REFACTORING_SUMMARY.md)** - Résumé des changements v2.0
- **[✨ Features](../microframe/FEATURES.md)** - Liste complète des fonctionnalités
- **[⚠️ Limitations](../microframe/LIMITATIONS.md)** - Limitations connues et roadmap
- **[🌍 Architecture Globale](ARCHITECTURE_GLOBAL.md)** - Vue d'ensemble système
- **[🔧 Technical README](TECHNICAL_README.md)** - Détails techniques

---

## 🎯 Par Type d'Utilisation

### Je veux créer une API REST

1. **[Getting Started](guides/getting-started.md)** - Concepts de base
2. **[Router](microframe/router.md)** - Organisation des routes
3. **[Validation](microframe/validation.md)** - Validation Pydantic
4. **[Dependencies](microframe/dependencies.md)** - Injection de dépendances

### Je veux ajouter l'authentification

1. **[Authentication Guide](guides/authentication.md)** - Guide complet AuthX
2. **[AuthX Overview](authx/intro.md)** - Documentation AuthX
3. **[JWT Tokens](authx/jwt.md)** - Gestion des tokens

### Je veux du temps réel (WebSocket)

1. **[WebSocket Chat Guide](guides/websocket-chat.md)** - Tutorial complet
2. **[WebSocket Manager](ws/websocket.md)** - Documentation WebSocket

### Je veux déployer en production

1. **[Deployment Guide](guides/deployment.md)** - Guide déploiement
2. **[Best Practices](guides/best-practices.md)** - Optimisations et sécurité
3. **[Configuration](microframe/configurations.md)** - Config production

---

## 🔍 Recherche Rapide

### Routing
- Créer une route : [Router](microframe/router.md#décorateurs-de-routes)
- Paramètres de route : [Router](microframe/router.md#paramètres-de-chemin)
- Routers modulaires : [Router](microframe/router.md#routers-imbriqués)

### Validation
- Valider body JSON : [Validation](microframe/validation.md#validation-body)
- Valider query params : [Validation](microframe/validation.md#query-parameters)
- Modèles Pydantic : [Validation](microframe/validation.md#pydantic-models)

### Authentification
- Setup AuthX : [Authentication Guide](guides/authentication.md#installation)
- Route protégée : [Authentication Guide](guides/authentication.md#routes-protégées)
- Custom AuthManager : [Auth Manager](authx/manager.md)

### WebSocket
- Setup WebSocket : [WebSocket Guide](guides/websocket-chat.md#setup)
- Authentification WS : [WebSocket](ws/websocket.md#authentication)
- Broadcast messages : [WebSocket Guide](guides/websocket-chat.md#broadcasting)

---

## 🤝 Contribution

La documentation est un projet vivant ! Pour contribuer :

1. **Signaler erreurs** : Ouvrir une [issue GitHub](https://github.com/traoreera/microframe/issues)
2. **Améliorer docs** : Pull request sur fichiers `.md`
3. **Ajouter exemples** : Contribuer au dossier `examples/`

**Guidelines** :
- Markdown pur (pas de HTML sauf nécessaire)
- Exemples testables et copy-pastables
- Français clair et concis
- Liens relatifs entre docs

---

## 📞 Support et Ressources

- **GitHub** : [traoreera/microframe](https://github.com/traoreera/microframe)
- **Issues** : [Bug reports & features](https://github.com/traoreera/microframe/issues)
- **Discussions** : [Questions & discussions](https://github.com/traoreera/microframe/discussions)

---

## 📄 License

MicroFrame est distribué sous [licence MIT](../LICENSE).

---

**Version Documentation** : 2.0.0  
**Dernière mise à jour** : 2025-11-24  
**Mainteneur** : [@traoreera](https://github.com/traoreera)

---

## 📖 Navigation Documentation

**📍 Vous êtes ici** : Index Documentation

**Commencer le parcours** : [Getting Started →](guides/getting-started.md)

### Parcours Complet
1. **📍 Index** (vous êtes ici)
2. [Getting Started](guides/getting-started.md)
3. [Authentication](guides/authentication.md)
4. [WebSocket Chat](guides/websocket-chat.md)
5. [Deployment](guides/deployment.md)
6. [Best Practices](guides/best-practices.md)

---

**[Commencer →](guides/getting-started.md)**
