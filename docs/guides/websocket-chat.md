# 🌐 Guide WebSocket Chat - Temps Réel

> Guide complet pour créer une application de chat temps réel avec WebSocket et authentification JWT

## 📋 Prérequis

- MicroFrame installé
- AuthX configuré (voir [Authentication Guide](authentication.md))
- Compréhension des WebSockets

---

## 🎯 Ce que vous allez construire

Une application de chat complète avec :
- ✅ Authentification JWT pour WebSocket
- ✅ Rooms/channels de discussion
- ✅ Broadcasting de messages
- ✅ Notifications connexion/déconnexion
- ✅ Messages privés

---

## 🚀 Setup WebSocket

### 1. Importer les Classes

```python
from microframe import Application
from microframe.ws import BaseWebSocket, ChatBase
from microframe.authx import AuthConfig, AuthManager
from starlette.routing import WebSocketRoute
```

### 2. Configuration

```python
from microframe.authx import AuthConfig
from auth_manager import MyAuthManager

# Configuration AuthX (pour auth WebSocket)
auth_config = AuthConfig(
    secret_key="votre-cle-secrete",
    algorithm="HS256"
)

auth_manager = MyAuthManager()

# Configurer WebSocket avec AuthX
ChatBase.configure(
    auth_config=auth_config,
    auth_manager=auth_manager
)
```

---

## 💬 Chat Simple

### WebSocket de Base

```python
from microframe.ws import ChatBase

class SimpleChatWebSocket(ChatBase):
    """Chat simple avec broadcast"""
    
    async def on_connect(self, websocket, user_id):
        """Appelé quand un user se connecte"""
        print(f"User {user_id} connected")
        
        # Notifier tous les autres
        await self.broadcast({
            "type": "user_joined",
            "user_id": user_id,
            "message": f"User {user_id} a rejoint le chat"
        }, exclude=[user_id])
    
    async def on_message(self, websocket, user_id, message):
        """Traiter les messages reçus"""
        print(f"Message from {user_id}: {message}")
        
        # Broadcaster à tous
        await self.broadcast({
            "type": "chat_message",
            "from": user_id,
            "text": message.get("text"),
            "timestamp": datetime.now().isoformat()
        })
    
    async def on_disconnect(self, websocket, user_id):
        """Appelé quand un user se déconnecte"""
        print(f"User {user_id} disconnected")
        
        # Notifier la déconnexion
        await self.broadcast({
            "type": "user_left",
            "user_id": user_id,
            "message": f"User {user_id} a quitté le chat"
        })

# Ajouter la route WebSocket
app = Application()
app.routes.append(
    WebSocketRoute("/ws/chat", SimpleChatWebSocket())
)
```

---

## 🔐 Authentification WebSocket

### Stratégies d'Authentification

Le `BaseWebSocket` supporte 3 méthodes d'auth :

#### 1. Query Parameter

```javascript
// Client JavaScript
const token = "eyJhbGc...";
const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
```

#### 2. Cookie

```javascript
// Le token est dans un cookie httpOnly
const ws = new WebSocket("ws://localhost:8000/ws/chat");
// Cookie automatiquement envoyé
```

#### 3. Sec-WebSocket-Protocol Header

```javascript
const token = "eyJhbGc...";
const ws = new WebSocket("ws://localhost:8000/ws/chat", [`token.${token}`]);
```

---

## 🏠 Rooms et Channels

### Chat avec Rooms

```python
class RoomChatWebSocket(ChatBase):
    """Chat avec support des rooms/channels"""
    
    async def on_connect(self, websocket, user_id):
        """Au connect, rejoindre room par défaut"""
        # Rejoindre la room "general"
        self.join_room(user_id, "general")
        
        # Notifier la room
        await self.broadcast_to_room("general", {
            "type": "user_joined_room",
            "user_id": user_id,
            "room": "general"
        }, exclude=[user_id])
    
    async def on_message(self, websocket, user_id, message):
        """Traiter les messages"""
        msg_type = message.get("type")
        
        if msg_type == "join_room":
            # Rejoindre une room
            room = message.get("room")
            self.join_room(user_id, room)
            
            await websocket.send_json({
                "type": "joined_room",
                "room": room,
                "members": self.get_room_members(room)
            })
            
            # Notifier les autres dans la room
            await self.broadcast_to_room(room, {
                "type": "user_joined_room",
                "user_id": user_id,
                "room": room
            }, exclude=[user_id])
        
        elif msg_type == "leave_room":
            # Quitter une room
            room = message.get("room")
            self.leave_room(user_id, room)
            
            await self.broadcast_to_room(room, {
                "type": "user_left_room",
                "user_id": user_id,
                "room": room
            })
        
        elif msg_type == "chat_message":
            # Message dans une room
            room = message.get("room")
            text = message.get("text")
            
            await self.broadcast_to_room(room, {
                "type": "room_message",
                "from": user_id,
                "room": room,
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
        
        elif msg_type == "private_message":
            # Message privé à un user
            to_user = message.get("to")
            text = message.get("text")
            
            await self.send_to(to_user, {
                "type": "private_message",
                "from": user_id,
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
```

---

## 💻 Client JavaScript

### Client Complet

```html
<!DOCTYPE html>
<html>
<head>
    <title>MicroFrame Chat</title>
</head>
<body>
    <div id="messages"></div>
    <input id="messageInput" type="text" placeholder="Message...">
    <button onclick="sendMessage()">Send</button>
    
    <script>
        // Token JWT (récupéré depuis login)
        const token = localStorage.getItem('access_token');
        
        // Connexion WebSocket
        const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
        
        ws.onopen = () => {
            console.log('Connected to chat');
            addMessage('System', 'Connecté au chat');
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleMessage(data);
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        ws.onclose = () => {
            console.log('Disconnected');
            addMessage('System', 'Déconnecté');
        };
        
        function handleMessage(data) {
            switch(data.type) {
                case 'user_joined':
                    addMessage('System', data.message);
                    break;
                
                case 'user_left':
                    addMessage('System', data.message);
                    break;
                
                case 'chat_message':
                    addMessage(data.from, data.text);
                    break;
                
                case 'room_message':
                    addMessage(`${data.from} [${data.room}]`, data.text);
                    break;
                
                case 'private_message':
                    addMessage(`${data.from} (privé)`, data.text);
                    break;
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            
            if (text) {
                ws.send(JSON.stringify({
                    type: 'chat_message',
                    text: text
                }));
                input.value = '';
            }
        }
        
        function addMessage(from, text) {
            const div = document.getElementById('messages');
            div.innerHTML += `<p><strong>${from}:</strong> ${text}</p>`;
            div.scrollTop = div.scrollHeight;
        }
        
        // Envoyer avec Enter
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

---

## 🎮 Exemple Complet avec Rooms

### Backend

```python
from microframe import Application
from microframe.ws import ChatBase
from microframe.authx import AuthConfig
from auth_manager import MyAuthManager
from starlette.routing import WebSocketRoute
from datetime import datetime

# Configuration
auth_config = AuthConfig(secret_key="secret")
auth_manager = MyAuthManager()

ChatBase.configure(auth_config=auth_config, auth_manager=auth_manager)

class AdvancedChatWebSocket(ChatBase):
    """Chat avancé avec rooms et features"""
    
    async def on_connect(self, websocket, user_id):
        # Get user info
        user = await self.auth_manager.get_user_by_id(user_id)
        
        # Join default room
        self.join_room(user_id, "lobby")
        
        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "user_id": user_id,
            "username": user.data.get("name"),
            "online_users": self.get_connected_users(),
            "rooms": list(self.rooms.keys())
        })
        
        # Notify lobby
        await self.broadcast_to_room("lobby", {
            "type": "user_joined",
            "user_id": user_id,
            "username": user.data.get("name")
        }, exclude=[user_id])
    
    async def on_message(self, websocket, user_id, message):
        msg_type = message.get("type")
        
        if msg_type == "join_room":
            room = message.get("room")
            self.join_room(user_id, room)
            
            # Confirm join
            await websocket.send_json({
                "type": "joined_room",
                "room": room,
                "members": self.get_room_members(room)
            })
            
            # Notify room
            user = await self.auth_manager.get_user_by_id(user_id)
            await self.broadcast_to_room(room, {
                "type": "user_joined_room",
                "user_id": user_id,
                "username": user.data.get("name"),
                "room": room
            }, exclude=[user_id])
        
        elif msg_type == "leave_room":
            room = message.get("room")
            self.leave_room(user_id, room)
            
            user = await self.auth_manager.get_user_by_id(user_id)
            await self.broadcast_to_room(room, {
                "type": "user_left_room",
                "user_id": user_id,
                "username": user.data.get("name"),
                "room": room
            })
        
        elif msg_type == "room_message":
            room = message.get("room")
            text = message.get("text")
            
            user = await self.auth_manager.get_user_by_id(user_id)
            await self.broadcast_to_room(room, {
                "type": "room_message",
                "from": user_id,
                "username": user.data.get("name"),
                "room": room,
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
        
        elif msg_type == "private_message":
            to_user_id = message.get("to")
            text = message.get("text")
            
            user = await self.auth_manager.get_user_by_id(user_id)
            
            # Send to recipient
            sent = await self.send_to(to_user_id, {
                "type": "private_message",
                "from": user_id,
                "username": user.data.get("name"),
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
            
            # Confirm to sender
            await websocket.send_json({
                "type": "private_message_sent",
                "to": to_user_id,
                "delivered": sent
            })
        
        elif msg_type == "typing":
            room = message.get("room")
            user = await self.auth_manager.get_user_by_id(user_id)
            
            # Notify others in room
            await self.broadcast_to_room(room, {
                "type": "user_typing",
                "user_id": user_id,
                "username": user.data.get("name"),
                "room": room
            }, exclude=[user_id])
    
    async def on_disconnect(self, websocket, user_id):
        user = await self.auth_manager.get_user_by_id(user_id)
        
        # Notify all rooms
        for room in self.get_user_rooms(user_id):
            await self.broadcast_to_room(room, {
                "type": "user_left",
                "user_id": user_id,
                "username": user.data.get("name") if user else "Unknown"
            })

# Application
app = Application()
app.routes.append(WebSocketRoute("/ws/chat", AdvancedChatWebSocket()))
```

---

## 🔧 Utilitaires WebSocket

### Méthodes Disponibles

```python
# Connexions
ChatBase.get_connected_users()  # Liste des user_ids connectés
ChatBase.is_connected(user_id)  # Vérifier si connecté
ChatBase.connection_count()     # Nombre total de connexions

# Rooms
ChatBase.get_room_members(room)  # Membres d'une room
ChatBase.get_user_rooms(user_id) # Rooms d'un user
ChatBase.join_room(user_id, room)
ChatBase.leave_room(user_id, room)

# Messaging
await ChatBase.broadcast(message, exclude=[])          # À tous
await ChatBase.send_to(user_id, message)               # À un user
await ChatBase.send_to_many(user_ids, message)         # À plusieurs
await ChatBase.broadcast_to_room(room, message, exclude=[])  # À une room
```

---

## 🐛 Debugging et Tests

### Tests WebSocket

```python
import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

def test_websocket_connection():
    """Test connexion WebSocket"""
    client = TestClient(app)
    
    with client.websocket_connect("/ws/chat?token=valid_token") as websocket:
        # Receive welcome message
        data = websocket.receive_json()
        assert data["type"] == "welcome"
        
        # Send message
        websocket.send_json({
            "type": "chat_message",
            "text": "Hello!"
        })
        
        # Should broadcast back
        response = websocket.receive_json()
        assert response["type"] == "chat_message"
        assert response["text"] == "Hello!"
```

---

## 📖 Prochaines Étapes

- **[Deployment](deployment.md)** - Déployer votre chat en production
- **[Best Practices](best-practices.md)** - Optimiser et sécuriser

---

---

## 📖 Navigation

**Parcours Documentation** :
1. [Index](../README.md)
2. [Getting Started](getting-started.md)
3. [Authentication](authentication.md)
4. **📍 WebSocket Chat** (vous êtes ici)
5. [Deployment](deployment.md)
6. [Best Practices](best-practices.md)

---

**[← Authentication](authentication.md)** | **[Index](../README.md)** | **[Deployment →](deployment.md)**
