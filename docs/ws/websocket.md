## 🌐 WebSocket Manager with JWT Authentication

The `BaseWebSocket` class provides a ready-to-use WebSocket manager with **JWT authentication**, connection management, and room/group support.
It is designed to integrate seamlessly with `Starlette` or any ASGI framework.

---

### 🔑 Features

* **JWT authentication** (access token via query, cookie, or header)
* User connection tracking by `user_id`
* Room/group management
* Broadcasting messages to all users
* Targeted messages to specific users
* Extensible hooks: `on_connect`, `on_message`, `on_disconnect`

---

### ⚙️ Setup

Before using, configure the WebSocket with `AuthX`:

```python
BaseWebSocket.configure(auth_config=config, auth_manager=manager)
```

---

### 🔒 Authentication

`authenticate(websocket)` performs:

1. Query parameter check: `?token=xxx`
2. Cookie check: `access_token`
3. Header `Sec-WebSocket-Protocol`: supports `token.xxx`

It validates:

* Token signature and type (`access`)
* Token expiration
* User existence via `AuthManager`

Raises `AuthenticationError` on failure.

---

### 🪝 Hooks

Override hooks for custom logic:

#### `on_connect(websocket, user_id)`

Triggered after a successful connection.

Use cases:

* Logging connections
* Sending welcome messages
* Adding users to default rooms

#### `on_message(websocket, user_id, message)`

Triggered for each incoming message.

> Must be implemented by subclasses.

#### `on_disconnect(websocket, user_id)`

Triggered on disconnection.

Use cases:

* Notify other users
* Remove from rooms
* Logging

---

### 🔄 Connection Management

Class methods:

| Method                    | Description                                |
| ------------------------- | ------------------------------------------ |
| `get_connected_users()`   | Returns all currently connected `user_id`s |
| `is_connected(user_id)`   | Checks if a specific user is connected     |
| `get_room_members(room)`  | Returns list of members in a room          |
| `get_user_rooms(user_id)` | Returns rooms a user belongs to            |
| `connection_count()`      | Returns total number of active connections |

---

### 💻 Usage Example

```python
class MyWebSocket(BaseWebSocket):
    async def on_message(self, websocket, user_id, message):
        await websocket.send_json({"echo": message})

# In Starlette routing
from starlette.routing import WebSocketRoute

routes = [
    WebSocketRoute("/ws", MyWebSocket())
]
```

---

### ⚡ Notes

* Connections are tracked in-memory (`connections: Dict[user_id, WebSocket]`)
* Rooms are implemented as sets (`rooms: Dict[room_name, Set[user_id]]`)
* Designed for **async and concurrent environments**
* Works with any AuthManager compliant with `AuthX`

---

## 📖 Navigation

**Documentation WebSocket** :
- [WebSocket Manager](websocket.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guide WebSocket](../guides/websocket-chat.md)**
