# Note sur le Module WebSocket (ws/)

## 📦 Module WebSocket Complet Existant

Le module **WebSocket** existe et est **complètement fonctionnel** dans `microframe/ws/`. 

### ✅ Ce qui existe (217 lignes de code)

#### 1. **BaseWebSocket** - Classe de base complète
- Authentification JWT automatique intégrée
- 3 stratégies d'auth: query params, cookies, headers
- Hooks extensibles: `on_connect()`, `on_message()`, `on_disconnect()`
- Gestion des connexions par user_id
- Intégration AuthX (AuthConfig + AuthManager)

#### 2. **ChatBase** - Extension pour chat/messaging
- Broadcast à tous les clients
- Envoi ciblé à un user spécifique
- Envoi à plusieurs users
- Système de rooms/groupes
- `join_room()`, `leave_room()`, `broadcast_to_room()`

### 📁 Structure

```
microframe/ws/
├── __init__.py              # Exports: ChatBase, BaseWebSocket
├── websocket.py (217 lignes) # BaseWebSocket avec auth
└── roomBase.py (105 lignes)  # ChatBase avec broadcast/rooms
```

### 💡 Exemple d'utilisation

```python
from microframe import Application
from microframe.ws import ChatBase
from microframe.authx import AuthConfig, AuthManager
from starlette.routing import WebSocketRoute

# Configuration
ChatBase.configure(auth_config, auth_manager)

# Créer une classe WebSocket custom
class MyChatWebSocket(ChatBase):
    async def on_connect(self, websocket, user_id):
        # User connecté
        await self.broadcast({
            "type": "user_joined",
            "user_id": user_id
        })
    
    async def on_message(self, websocket, user_id, message):
        # Traiter le message
        if message["type"] == "chat":
            await self.broadcast({
                "from": user_id,
                "text": message["text"]
            })
        elif message["type"] == "join_room":
            self.join_room(user_id, message["room"])

# Route WebSocket
app = Application()
app.routes.append(
    WebSocketRoute("/ws/chat", MyChatWebSocket())
)
```

### 🎯 Fonctionnalités Complètes

✅ **Authentification JWT**
- Token via query: `?token=xxx`
- Token via cookie: `access_token`
- Token via header: `Sec-WebSocket-Protocol`

✅ **Gestion Connexions**
- `connections: Dict[user_id, WebSocket]`
- `get_connected_users()` - Liste des users
- `is_connected(user_id)` - Vérifier connexion
- `connection_count()` - Nombre total

✅ **Rooms/Groupes**
- `rooms: Dict[room_name, Set[user_ids]]`
- `join_room(user_id, room)` - Rejoindre
- `leave_room(user_id, room)` - Quitter
- `get_room_members(room)` - Liste membres
- `get_user_rooms(user_id)` - Rooms d'un user

✅ **Broadcasting**
- `broadcast(message, exclude=[])` - À tous
- `send_to(user_id, message)` - À un user
- `send_to_many(user_ids, message)` - À plusieurs
- `broadcast_to_room(room, message)` - À une room

✅ **Hooks Extensibles**
- `on_connect(websocket, user_id)` - Après connexion
- `on_message(websocket, user_id, message)` - Message reçu
- `on_disconnect(websocket, user_id)` - Déconnexion

### ❌ Ce qui manque (VRAIES limitations)

1. **Documentation**
   - Pas de ws/README.md
   - Pas mentionné dans README principal
   - Pas dans FEATURES.md

2. **Exemples**
   - Pas d'exemples dans examples/
   - Pas de guide d'utilisation
   - Pas de best practices

3. **Tests**
   - Pas de tests pour ws/
   - Pas de coverage
   - Non testé en intégration

4. **Export**
   - Pas dans `microframe/__init__.py`
   - Import direct nécessaire

5. **Fonctionnalités avancées**
   - Pas de reconnexion automatique
   - Pas de heartbeat/ping-pong
   - Pas de compression
   - Pas de binary messages support

### ✅ Correction LIMITATIONS.md

**Avant** (incorrect):
> "Pas de Support WebSocket Documenté" 
> "WebSockets supportés par Starlette mais non documentés"

**Après** (correct):
> "Module WebSocket - Documentation Manquante"
> "Le module WebSocket existe et est fonctionnel mais manque de documentation"

---

**Date**: 2025-11-23  
**Clarification pour**: LIMITATIONS.md v2.0.0  
**Module**: microframe/ws/
