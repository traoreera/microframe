from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AuthManager(ABC):
    """Abstract base class for user authentication management.
    
    Implement this class to provide custom user authentication logic.
    """

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by email and password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            Dictionary containing user data (must include 'id' key) if authentication succeeds,
            None otherwise.
            
        Example:
            {"id": "123", "email": "user@example.com", "name": "John Doe"}
        """
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: User's unique identifier

        Returns:
            Dictionary containing user data (must include 'id' and 'email' keys) if found,
            None otherwise.
        """
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by their email address.

        Args:
            email: User's email address

        Returns:
            Dictionary containing user data (must include 'id' and 'email' keys) if found,
            None otherwise.
        """
        pass
