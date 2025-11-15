from typing import Any, List, Optional

from .websocket import BaseWebSocket


class ChatBase(BaseWebSocket):

    @classmethod
    async def broadcast(cls, message: Any, exclude: Optional[List[str]] = None):
        """
        Envoie à tous les clients connectés

        Args:
            message: Données à envoyer (dict ou autre JSON serializable)
            exclude: Liste d'user_ids à exclure
        """
        exclude = exclude or []
        for user_id, ws in cls.connections.items():
            if user_id not in exclude:
                try:
                    await ws.send_json(message)
                except Exception:
                    pass  # Ignore si la connexion est morte

    @classmethod
    async def send_to(cls, user_id: str, message: Any):
        """
        Envoie à un utilisateur spécifique

        Args:
            user_id: ID de l'utilisateur cible
            message: Données à envoyer

        Returns:
            True si envoyé, False si user non connecté
        """
        if user_id in cls.connections:
            try:
                await cls.connections[user_id].send_json(message)
                return True
            except Exception:
                return False
        return False

    @classmethod
    async def send_to_many(cls, user_ids: List[str], message: Any):
        """
        Envoie à plusieurs utilisateurs

        Args:
            user_ids: Liste d'IDs cibles
            message: Données à envoyer
        """
        for user_id in user_ids:
            await cls.send_to(user_id, message)

    # ========== Gestion des rooms/groupes ==========
    @classmethod
    def join_room(cls, user_id: str, room: str):
        """Ajoute un user à une room"""
        if room not in cls.rooms:
            cls.rooms[room] = set()
        cls.rooms[room].add(user_id)

    @classmethod
    def leave_room(cls, user_id: str, room: str):
        """Retire un user d'une room"""
        if room in cls.rooms:
            cls.rooms[room].discard(user_id)
            if not cls.rooms[room]:
                del cls.rooms[room]

    @classmethod
    def _remove_from_all_rooms(cls, user_id: str):
        """Retire un user de toutes les rooms"""
        if not user_id:
            return
        rooms_to_clean = []
        for room, members in cls.rooms.items():
            if user_id in members:
                members.discard(user_id)
                if not members:
                    rooms_to_clean.append(room)

        for room in rooms_to_clean:
            del cls.rooms[room]

    @classmethod
    async def broadcast_to_room(cls, room: str, message: Any, exclude: Optional[List[str]] = None):
        """
        Envoie à tous les membres d'une room

        Args:
            room: Nom de la room
            message: Données à envoyer
            exclude: User IDs à exclure
        """
        if room not in cls.rooms:
            return

        exclude = exclude or []
        for user_id in cls.rooms[room]:
            if user_id not in exclude:
                await cls.send_to(user_id, message)
