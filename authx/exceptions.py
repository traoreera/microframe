class AuthException(Exception):
    """Exception de base pour les erreurs d'authentification"""

    def __init__(self, message: str = "Erreur d'authentification", status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class CredentialsException(AuthException):
    """Exception pour des identifiants invalides"""

    def __init__(self, message: str = "Identifiants invalides"):
        super().__init__(message, 401)


class InvalidTokenException(AuthException):
    """Exception pour un token invalide"""

    def __init__(self, message: str = "Token invalide"):
        super().__init__(message, 401)


class TokenExpiredException(AuthException):
    """Exception pour un token expiré"""

    def __init__(self, message: str = "Token expiré"):
        super().__init__(message, 401)


class UserNotFoundException(AuthException):
    """Exception pour utilisateur non trouvé"""

    def __init__(self, message: str = "Utilisateur non trouvé"):
        super().__init__(message, 404)
