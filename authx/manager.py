from abc import ABC, abstractmethod
from typing import Annotated, Any, Optional

from annotated_types import doc

from authx.models import UserResponse


class AuthManager(ABC):
    """Classe abstraite pour la gestion des utilisateurs"""

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        Récupère un utilisateur par son email

        Args:
            email: Email de l'utilisateur

        Returns:
            UserResponse si trouvé, None sinon
        """

    @abstractmethod
    async def get_user_by_id(
        self, user_id: Annotated[Any, doc("ID de l'utilisateur")]
    ) -> Optional[UserResponse]:
        """
        Récupère un utilisateur par son ID

        Args:
            user_id: ID de l'utilisateur

        Returns:
            UserResponse si trouvé, None sinon
        """

    @abstractmethod
    async def verify_password(self, email: str, password: str) -> bool:
        """
        Vérifie le mot de passe d'un utilisateur

        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair

        Returns:
            True si le mot de passe est correct, False sinon
        """

    async def authenticate(self, email: str, password: str) -> Optional[UserResponse]:
        """
        Authentifie un utilisateur

        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair

        Returns:
            UserResponse si authentifié, None sinon
        """
        if await self.verify_password(email, password):
            return await self.get_user_by_email(email)
        return None
