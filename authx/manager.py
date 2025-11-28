from abc import ABC, abstractmethod

from authx.models import LoginRequest, UserResponse


class AuthManager(ABC):
    """Classe abstraite pour la gestion des utilisateurs"""

    @abstractmethod
    async def verified_user(self, user: LoginRequest) -> UserResponse:
        """
        Récupère un utilisateur par son email

        Args:
            email: Email de l'utilisateur

        Returns:
            UserResponse si найд, None sinon
        """
