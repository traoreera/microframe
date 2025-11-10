# microframework/dependencies.py
"""
Système Depends amélioré similaire à FastAPI
"""
import inspect
from typing import Callable, Any, Dict, Optional, get_type_hints
from functools import wraps
from starlette.requests import Request
from pydantic import BaseModel, ValidationError

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
    
    def __init__(
        self,
        dependency: Callable,
        *,
        use_cache: bool = True
    ):
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
    
    async def resolve(self, func: Callable, request: Request) -> Dict[str, Any]:
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
        type_hints = get_type_hints(func)
        
        for param_name, param in sig.parameters.items():
            # Ignorer request et self
            if param_name in ["request", "self"]:
                continue
            
            # Cas 1: Depends() explicite
            if isinstance(param.default, Depends):
                dep_value = await self._resolve_depends(
                    param.default,
                    request,
                    param_name
                )
                deps[param_name] = dep_value
            
            # Cas 2: Dépendance enregistrée par nom
            elif param_name in self._dependencies:
                dep_value = await self._resolve_named_dependency(
                    param_name,
                    request
                )
                deps[param_name] = dep_value
            
            # Cas 3: Annotation de type qui est une dépendance
            elif param_name in type_hints:
                type_hint = type_hints[param_name]
                if callable(type_hint) and hasattr(type_hint, '__call__'):
                    # Essayer de résoudre comme une dépendance
                    try:
                        dep_value = await self._call_dependency(type_hint, request)
                        deps[param_name] = dep_value
                    except Exception:
                        # Pas une dépendance valide, ignorer
                        pass
        
        return deps
    
    async def _resolve_depends(
        self,
        depends: Depends,
        request: Request,
        param_name: str
    ) -> Any:
        """Résout une dépendance Depends()"""
        
        # Vérifier le cache si activé
        if depends.use_cache and depends._cache_key in self._cache:
            return self._cache[depends._cache_key]
        
        # Vérifier les dépendances circulaires
        dep_id = id(depends.dependency)
        if dep_id in self._solving:
            raise RuntimeError(
                f"Dépendance circulaire détectée: {depends.dependency.__name__}"
            )
        
        self._solving.add(dep_id)
        
        try:
            # Résoudre les sous-dépendances de la dépendance
            sub_deps = await self.resolve(depends.dependency, request)
            
            # Ajouter request si nécessaire
            if "request" in inspect.signature(depends.dependency).parameters:
                sub_deps["request"] = request
            
            # Appeler la dépendance
            result = await self._call_dependency(depends.dependency, request, **sub_deps)
            
            # Mettre en cache si nécessaire
            if depends.use_cache:
                self._cache[depends._cache_key] = result
            
            return result
        
        finally:
            self._solving.discard(dep_id)
    
    async def _resolve_named_dependency(
        self,
        name: str,
        request: Request
    ) -> Any:
        """Résout une dépendance enregistrée par nom"""
        
        # Vérifier le cache
        if name in self._cache and self._cache[name] is not None:
            return self._cache[name]
        
        dep_func = self._dependencies[name]
        
        # Résoudre les sous-dépendances
        sub_deps = await self.resolve(dep_func, request)
        
        # Ajouter request si nécessaire
        if "request" in inspect.signature(dep_func).parameters:
            sub_deps["request"] = request
        
        # Appeler la dépendance
        result = await self._call_dependency(dep_func, request, **sub_deps)
        
        # Mettre en cache si configuré
        if name in self._cache:
            self._cache[name] = result
        
        return result
    
    async def _call_dependency(
        self,
        func: Callable,
        request: Request = None,
        **kwargs
    ) -> Any:
        """Appelle une dépendance (sync ou async)"""
        
        # Vérifier si la fonction accepte request
        sig = inspect.signature(func)
        if "request" in sig.parameters and request is not None:
            kwargs["request"] = request
        
        # Appeler la fonction
        if inspect.iscoroutinefunction(func):
            return await func(**kwargs)
        return func(**kwargs)
    
    def clear_cache(self):
        """Vide le cache des dépendances"""
        self._cache.clear()


# =============================================================
# Dépendances communes utiles
# =============================================================

class Pagination:
    """Dépendance pour la pagination"""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        max_limit: int = 1000
    ):
        self.skip = max(0, skip)
        self.limit = min(limit, max_limit)
    
    @property
    def offset(self):
        return self.skip
    
    def __repr__(self):
        return f"Pagination(skip={self.skip}, limit={self.limit})"


def get_pagination(
    skip: int = 0,
    limit: int = 100
) -> Pagination:
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
# Exemples d'utilisation
# =============================================================

def example_usage():
    """Exemples d'utilisation du système Depends"""
    
    # Exemple 1: Dépendance simple
    def get_current_time():
        from datetime import datetime
        return datetime.now()
    
    # Dans une route:
    # async def route(current_time = Depends(get_current_time)):
    #     return {"time": current_time}
    
    # Exemple 2: Dépendance avec sous-dépendances
    def get_user_service(db = Depends(get_db)):
        class UserService:
            def __init__(self, db):
                self.db = db
            
            def get_all_users(self):
                return self.db.query("User")
        
        return UserService(db)
    
    # Dans une route:
    # async def route(user_service = Depends(get_user_service)):
    #     return user_service.get_all_users()
    
    # Exemple 3: Dépendance avec paramètres
    def get_query_params(request: Request):
        return dict(request.query_params)
    
    # Exemple 4: Dépendance conditionnelle
    def get_admin_user(user = Depends(get_current_user)):
        if not user.is_admin:
            raise Exception("Not admin")
        return user
    
    # Dans une route admin:
    # async def admin_route(admin = Depends(get_admin_user)):
    #     return {"admin": admin}


class AppException(Exception):
    """Exception de base pour l'application"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        return {
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details
        }


class RequestValidator:
    """Validateur de requêtes avec Pydantic"""
    
    @staticmethod
    async def parse_request(request: Request, func: Callable) -> Dict[str, Any]:
        """Parse et valide les données de la requête"""
        sig = inspect.signature(func)
        values = {}
        
        # Query parameters
        query_params = dict(request.query_params)
        
        # Body data
        body_data = {}
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    body_data = await request.json()
            except Exception as e:
                logger.error(f"Erreur parsing JSON: {e}")
                raise AppException(
                    "Invalid JSON in request body",
                    status_code=400,
                    details={"error": str(e)}
                )
        
        # Résolution des paramètres
        for param_name, param in sig.parameters.items():
            ann = param.annotation
            
            # Model Pydantic
            if RequestValidator._is_pydantic_model(ann):
                try:
                    values[param_name] = ann(**body_data)
                except ValidationError as e:
                    raise AppException(
                        "Validation error",
                        status_code=422,
                        details={"errors": e.errors()}
                    )
            # Query parameter
            elif param_name in query_params:
                values[param_name] = query_params[param_name]
            # Request object
            elif param_name == "request":
                values[param_name] = request
            # Paramètre avec valeur par défaut
            elif param.default != inspect.Parameter.empty:
                values[param_name] = param.default
        
        return values
    
    @staticmethod
    def _is_pydantic_model(cls) -> bool:
        """Vérifie si une classe est un modèle Pydantic"""
        try:
            return issubclass(cls, BaseModel)
        except TypeError:
            return False
