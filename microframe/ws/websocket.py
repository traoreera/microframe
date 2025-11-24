from typing import Any, Dict, List, Optional, Set

from starlette.authentication import AuthenticationError
from starlette.websockets import WebSocket, WebSocketDisconnect

from authx.config import AuthConfig
from authx.exceptions import InvalidTokenException, TokenExpiredException
from authx.jwt import decode_token
from authx.manager import AuthManager


class BaseWebSocket:
    """
    WebSocket manager avec authentification JWT intégrée

    Fonctionnalités:
    - Authentification automatique via JWT
    - Gestion des connexions par user_id
    - Broadcast à tous les clients
    - Envoi ciblé à un utilisateur
    - Groupes/rooms pour organisation
    - Hooks extensibles (on_connect, on_message, on_disconnect)
    """

    # Connexions: {user_id: WebSocket}
    connections: Dict[str, WebSocket] = {}

    # Groupes/rooms: {room_name: Set[user_id]}
    rooms: Dict[str, Set[str]] = {}

    # Configuration AuthX (à injecter)
    auth_config: Optional[AuthConfig] = None
    auth_manager: Optional[AuthManager] = None

    @classmethod
    def configure(cls, auth_config: AuthConfig, auth_manager: AuthManager):
        """Configure le WebSocket avec AuthX"""
        cls.auth_config = auth_config
        cls.auth_manager = auth_manager

    async def authenticate(self, websocket: WebSocket) -> Optional[str]:
        """
        Authentifie le WebSocket via JWT

        Stratégies d'authentification (par ordre de priorité):
        1. Query param: ?token=xxx
        2. Cookie: refresh_token ou access_token
        3. Header Sec-WebSocket-Protocol

        Args:
            websocket: WebSocket Starlette

        Returns:
            user_id si authentifié, None pour public

        Raises:
            AuthenticationError: Si token invalide/expiré
        """
        # Stratégie 1: Query param
        token = websocket.query_params.get("token")

        # Stratégie 2: Cookie
        if not token:
            token = websocket.cookies.get("access_token")

        # Stratégie 3: Sec-WebSocket-Protocol header
        if not token:
            protocols = websocket.headers.get("sec-websocket-protocol", "")
            if protocols:
                # Format: "token.eyJhbGc..."
                parts = protocols.split(",")
                for part in parts:
                    if part.strip().startswith("token."):
                        token = part.strip().replace("token.", "")
                        break

        if not token:
            raise AuthenticationError("Missing authentication token")

        # Vérifier le token avec AuthX
        if not self.auth_config:
            raise RuntimeError("WebSocket not configured. Call BaseWebSocket.configure() first")

        try:
            payload = decode_token(token, self.auth_config, "access")
            user_id = payload.get("sub")

            if not user_id:
                raise AuthenticationError("Invalid token payload")

            # Vérifier que l'utilisateur existe
            if self.auth_manager:
                user = await self.auth_manager.get_user_by_id(user_id)
                if not user:
                    raise AuthenticationError("User not found")

            return user_id

        except (InvalidTokenException, TokenExpiredException) as e:
            return AuthenticationError(str(e))

    async def on_connect(self, websocket: WebSocket, user_id: Optional[str]):
        """
        Hook appelé après connexion réussie

        Override ce hook pour ajouter une logique custom:
        - Logger la connexion
        - Envoyer un message de bienvenue
        - Ajouter à des rooms par défaut

        Args:
            websocket: WebSocket connecté
            user_id: ID de l'utilisateur authentifié
        """

    async def on_message(self, websocket: WebSocket, user_id: Optional[str], message: Any):
        """
        Hook appelé à chaque message reçu

        DOIT être overridé pour traiter les messages

        Args:
            websocket: WebSocket émetteur
            user_id: ID de l'utilisateur
            message: Données reçues (déjà parsées en JSON)
        """
        raise NotImplementedError("on_message must be implemented")

    async def on_disconnect(self, websocket: WebSocket, user_id: Optional[str]):
        """
        Hook appelé lors de la déconnexion

        Override pour cleanup:
        - Notifier les autres users
        - Retirer des rooms
        - Logger la déconnexion

        Args:
            websocket: WebSocket déconnecté
            user_id: ID de l'utilisateur
        """

    async def on_receive(self, websocket: WebSocket, user_id: Optional[str], message: Any):
        """
        Hook appelé par le routing Starlette

        Args:
            websocket: WebSocket connecté
            user_id: ID de l'utilisateur authentifié
            message: Données reçues (déja parsées en JSON)
        """

    async def __call__(self, websocket: WebSocket):
        """
        Entry point utilisé par le routing Starlette

        WebSocketRoute("/ws", MyWebSocket())
        """
        await websocket.accept()
        user_id = None

        try:
            # Authentification
            try:
                user_id = await self.authenticate(websocket)
            except AuthenticationError as e:
                await websocket.send_json({"error": str(e)})
                await websocket.close(code=4401)
                return

            # Enregistrer la connexion
            self.connections[user_id] = websocket

            # Hook de connexion
            await self.on_connect(websocket, user_id)

            # Boucle de réception des messages
            while True:
                data = await websocket.receive_json()
                await self.on_message(websocket, user_id, data)

        except WebSocketDisconnect:
            pass
        finally:
            # Cleanup
            await self.on_disconnect(websocket, user_id)
            if user_id and user_id in self.connections:
                del self.connections[user_id]

            # Retirer des rooms
            self._remove_from_all_rooms(user_id)

    @classmethod
    def get_connected_users(cls) -> List[str]:
        """Retourne la liste des user_ids connectés"""
        return list(cls.connections.keys())

    @classmethod
    def is_connected(cls, user_id: str) -> bool:
        """Vérifie si un user est connecté"""
        return user_id in cls.connections

    @classmethod
    def get_room_members(cls, room: str) -> List[str]:
        """Retourne les membres d'une room"""
        return list(cls.rooms.get(room, set()))

    @classmethod
    def get_user_rooms(cls, user_id: str) -> List[str]:
        """Retourne les rooms d'un user"""
        return [room for room, members in cls.rooms.items() if user_id in members]

    @classmethod
    def connection_count(cls) -> int:
        """Retourne le nombre de connexions actives"""
        return len(cls.connections)
