# Note sur le Module AuthX

## 📦 Architecture Modulaire Intentionnelle

Le module **AuthX** est un **module optionnel séparé** de MicroFrame core. Cette séparation est une **décision architecturale intentionnelle** et non une limitation.

### Avantages de cette Architecture

✅ **Maintenabilité améliorée**
- AuthX peut évoluer indépendamment du core
- Versions et releases séparées
- Tests isolés

✅ **Installation optionnelle**
- Les projets sans authentification n'ont pas besoin d'installer AuthX
- Réduction de la taille d'installation pour projets simples
- Dépendances auth isolées (jose, bcrypt, etc.)

✅ **Flexibilité**
- Utilisateurs peuvent choisir leur propre système d'auth
- AuthX n'est qu'une option parmi d'autres
- Pas de couplage forcé

✅ **Spécialisation**
- AuthX peut se concentrer uniquement sur l'authentification
- Documentation et exemples dédiés
- Équipe de maintenance potentiellement séparée

### Ce qui change dans LIMITATIONS.md

Les points suivants dans LIMITATIONS.md sont à reconsidérer :

**❌ NE SONT PAS des limitations** :
- "AuthX non intégré avec Core" → C'est intentionnel
- "Pas dans microframe/__init__.py" → Normal pour module séparé
- "Documentation séparée" → Avantage d'avoir docs dédiées

**✅ SONT des vraies limitations** :
- Système Depends dupliqu (authx.Depends vs microframe.Depends)
- Pas de RBAC/permissions
- Pas d'OAuth2 flow
- Pas de token rotation/blacklist
- Pas de 2FA/MFA

### Comment documenter correctement

Au lieu de présenter AuthX comme "non intégré" (négatif), il faut présenter comme :

> **AuthX** est un module d'authentification optionnel séparé, installable indépendamment. 
> Cette architecture modulaire facilite la maintenabilité.
> 
> **Installation** : `pip install microframe-authx`
> 
> **Limitations actuelles** :
> - Système Depends non unifié avec core
> - RBAC manquant
> - OAuth2 flows manquants
> - Pas de 2FA/MFA

---

**Date**: 2025-11-23  
**Clarification pour**: LIMITATIONS.md v2.0.0
