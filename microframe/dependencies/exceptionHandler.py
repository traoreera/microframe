# microframework/dependencies.py
"""
Système Depends amélioré similaire à FastAPI - VERSION CORRIGÉE
"""
import inspect
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, get_type_hints

from pydantic import BaseModel, ValidationError
from starlette.requests import Request

logger = logging.getLogger(__name__)


class Depends:
    """
    Marqueur de dépendance pour l'injection automatique

    Usage:
        def get_db():
            return Database()

        @app.route("/users")
        async def get_users(db = Depends(get_db)):
            return db.query(User).all()
    """

    def __init__(self, dependency: Callable, *, use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache
        self._cache_key = f"depends_{id(dependency)}"

    def __repr__(self):
        return f"Depends({self.dependency.__name__})"


class DependencyManager:
    """
    Gestionnaire avancé d'injection de dépendances avec support de Depends
    """

    def __init__(self):
        self._dependencies: Dict[str, Callable] = {}
        self._cache: Dict[str, Any] = {}
        self._solving = set()  # Pour détecter les dépendances circulaires

    def register(self, name: str, func: Callable, cache: bool = False):
        """Enregistre une dépendance via décorateur"""
        self._dependencies[name] = func
        if cache:
            self._cache[name] = None
        logger.debug(f"Dépendance enregistrée: {name}")

    async def resolve(self, func: Callable, request: Optional[Request] = None) -> Dict[str, Any]:
        """
        Résout toutes les dépendances d'une fonction, incluant Depends

        Supporte:
        - Dépendances nommées (enregistrées via @dependency)
        - Dépendances Depends() (style FastAPI)
        - Dépendances imbriquées (récursives)
        - Cache des résultats
        - Détection des dépendances circulaires
        """
        deps = {}
        sig = inspect.signature(func)

        # Obtenir les type hints de manière sûre
        try:
            get_type_hints(func)
        except Exception as e:
            logger.debug(f"Impossible d'obtenir les type hints pour {func.__name__}: {e}")

        for param_name, param in sig.parameters.items():
            # Ignorer request et self
            if param_name in ["request", "self"]:
                continue

            # Cas 1: Depends() explicite
            if isinstance(param.default, Depends):
                logger.debug(f"Résolution de Depends pour {param_name}")
                dep_value = await self._resolve_depends(param.default, request, param_name)
                deps[param_name] = dep_value
                logger.debug(f"Depends résolu: {param_name} = {type(dep_value)}")

            # Cas 2: Dépendance enregistrée par nom
            elif param_name in self._dependencies:
                logger.debug(f"Résolution de dépendance nommée: {param_name}")
                dep_value = await self._resolve_named_dependency(param_name, request)
                deps[param_name] = dep_value

        return deps

    async def _resolve_depends(
        self, depends: Depends, request: Optional[Request], param_name: str
    ) -> Any:
        """Résout une dépendance Depends()"""

        # Vérifier le cache si activé
        if depends.use_cache and depends._cache_key in self._cache:
            logger.debug(f"Utilisation du cache pour {param_name}")
            return self._cache[depends._cache_key]

        # Vérifier les dépendances circulaires
        dep_id = id(depends.dependency)
        if dep_id in self._solving:
            raise RuntimeError(f"Dépendance circulaire détectée: {depends.dependency.__name__}")

        self._solving.add(dep_id)

        try:
            # Résoudre les sous-dépendances de la dépendance
            sub_deps = await self.resolve(depends.dependency, request)

            # Ajouter request si nécessaire
            sig = inspect.signature(depends.dependency)
            if "request" in sig.parameters and request is not None:
                sub_deps["request"] = request

            # Appeler la dépendance
            result = await self._call_dependency(depends.dependency, request, **sub_deps)

            # Mettre en cache si nécessaire
            if depends.use_cache:
                self._cache[depends._cache_key] = result

            logger.debug(f"Dépendance résolue: {depends.dependency.__name__} -> {type(result)}")
            return result

        finally:
            self._solving.discard(dep_id)

    async def _resolve_named_dependency(self, name: str, request: Optional[Request]) -> Any:
        """Résout une dépendance enregistrée par nom"""

        # Vérifier le cache
        if name in self._cache and self._cache[name] is not None:
            return self._cache[name]

        dep_func = self._dependencies[name]

        # Résoudre les sous-dépendances
        sub_deps = await self.resolve(dep_func, request)

        # Ajouter request si nécessaire
        if "request" in inspect.signature(dep_func).parameters and request is not None:
            sub_deps["request"] = request

        # Appeler la dépendance
        result = await self._call_dependency(dep_func, request, **sub_deps)

        # Mettre en cache si configuré
        if name in self._cache:
            self._cache[name] = result

        return result

    async def _call_dependency(
        self, func: Callable, request: Optional[Request] = None, **kwargs
    ) -> Any:
        """Appelle une dépendance (sync ou async)"""

        # Vérifier si la fonction accepte request
        sig = inspect.signature(func)
        call_kwargs = {}

        for param_name in sig.parameters:
            if param_name == "request" and request is not None:
                call_kwargs["request"] = request
            elif param_name in kwargs:
                call_kwargs[param_name] = kwargs[param_name]

        # Appeler la fonction
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(**call_kwargs)
            else:
                result = func(**call_kwargs)

            logger.debug(f"Dépendance appelée: {func.__name__} -> {type(result)}")
            return result
        except Exception as e:
            logger.error(f"Erreur lors de l'appel de {func.__name__}: {e}", exc_info=True)
            raise

    def clear_cache(self):
        """Vide le cache des dépendances"""
        self._cache.clear()
        logger.debug("Cache des dépendances vidé")


# =============================================================
# Dépendances communes utiles
# =============================================================


class Pagination:
    """Dépendance pour la pagination"""

    def __init__(self, skip: int = 0, limit: int = 100, max_limit: int = 1000):
        self.skip = max(0, skip)
        self.limit = min(limit, max_limit)

    @property
    def offset(self):
        return self.skip

    def __repr__(self):
        return f"Pagination(skip={self.skip}, limit={self.limit})"


def get_pagination(skip: int = 0, limit: int = 100) -> Pagination:
    """Dépendance de pagination réutilisable"""
    return Pagination(skip=skip, limit=limit)


class Settings:
    """Configuration de l'application"""

    def __init__(self):
        self.app_name = "MicroFramework"
        self.debug = True
        self.secret_key = "secret"


def get_settings() -> Settings:
    """
    Dépendance pour obtenir la configuration

    Usage:
        @app.route("/config")
        async def config(settings = Depends(get_settings)):
            return {"app_name": settings.app_name}
    """
    return Settings()


# =============================================================
# Décorateurs utilitaires
# =============================================================


def inject(*dependencies):
    """
    Décorateur pour injecter automatiquement des dépendances

    Usage:
        @inject(get_db, get_settings)
        async def my_function(db, settings):
            return {"db": db, "settings": settings}
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Résoudre les dépendances
            for dep in dependencies:
                dep_name = dep.__name__.replace("get_", "")
                if dep_name not in kwargs:
                    if inspect.iscoroutinefunction(dep):
                        kwargs[dep_name] = await dep()
                    else:
                        kwargs[dep_name] = dep()

            # Appeler la fonction
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# =============================================================
# Classes d'Exception et Validation
# =============================================================


class AppException(Exception):
    """Exception de base pour l'application"""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self):
        return {"message": self.message, "status_code": self.status_code, "details": self.details}
