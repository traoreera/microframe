# microframework/utils/logger.py
"""
Système de logging avancé avec rotation, formatage JSON et contexte
"""
import inspect
import json
import logging
import sys
import threading
import time
import traceback
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional

# =============================================================
# Configuration
# =============================================================


class LogConfig:
    """Configuration du système de logging"""

    def __init__(self):
        self.log_level = logging.INFO
        self.log_dir = Path("logs")
        self.log_format = "json"  # "json" ou "text"
        self.enable_console = True
        self.enable_file = True
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.backup_count = 5
        self.enable_rotation = True
        self.rotation_interval = "midnight"  # ou "H", "D", "W0"-"W6"
        self.enable_request_logging = True
        self.log_sql_queries = False
        self.sensitive_fields = ["password", "token", "secret", "api_key"]


# Instance globale de configuration
log_config = LogConfig()


# =============================================================
# Contexte de logging (thread-local)
# =============================================================


class LogContext:
    """Contexte thread-local pour le logging"""

    def __init__(self):
        self._local = threading.local()

    def set(self, key: str, value: Any):
        """Définit une valeur dans le contexte"""
        if not hasattr(self._local, "data"):
            self._local.data = {}
        self._local.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur du contexte"""
        if not hasattr(self._local, "data"):
            return default
        return self._local.data.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """Récupère tout le contexte"""
        if not hasattr(self._local, "data"):
            return {}
        return self._local.data.copy()

    def clear(self):
        """Vide le contexte"""
        if hasattr(self._local, "data"):
            self._local.data.clear()


# Instance globale du contexte
log_context = LogContext()


@contextmanager
def logging_context(**kwargs):
    """
    Context manager pour ajouter des données au contexte de logging

    Usage:
        with logging_context(user_id=123, request_id="abc"):
            logger.info("Action performed")
    """
    # Sauvegarder l'ancien contexte
    old_context = log_context.get_all()

    # Ajouter les nouvelles valeurs
    for key, value in kwargs.items():
        log_context.set(key, value)

    try:
        yield
    finally:
        # Restaurer l'ancien contexte
        log_context.clear()
        for key, value in old_context.items():
            log_context.set(key, value)


# =============================================================
# Formateurs personnalisés
# =============================================================


class JSONFormatter(logging.Formatter):
    """Formateur JSON pour les logs"""

    def format(self, record: logging.LogRecord) -> str:
        """Formate le log en JSON"""

        # Données de base
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Ajouter le contexte
        context = log_context.get_all()
        if context:
            log_data["context"] = context

        # Ajouter les champs extra
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Ajouter l'exception si présente
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Masquer les champs sensibles
        log_data = self._mask_sensitive_data(log_data)

        return json.dumps(log_data, ensure_ascii=False, default=str)

    def _mask_sensitive_data(self, data: Dict) -> Dict:
        """Masque les données sensibles"""
        if not isinstance(data, dict):
            return data

        masked_data = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in log_config.sensitive_fields):
                masked_data[key] = "***MASKED***"
            elif isinstance(value, dict):
                masked_data[key] = self._mask_sensitive_data(value)
            elif isinstance(value, list):
                masked_data[key] = [
                    self._mask_sensitive_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                masked_data[key] = value

        return masked_data


class ColoredFormatter(logging.Formatter):
    """Formateur avec couleurs pour la console"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Vert
        "WARNING": "\033[33m",  # Jaune
        "ERROR": "\033[31m",  # Rouge
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formate le log avec couleurs"""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Format de base
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        log_format = (
            f"{color}[{timestamp}] "
            f"{record.levelname:8s}{reset} "
            f"{record.name} - {record.getMessage()}"
        )

        # Ajouter le contexte si présent
        context = log_context.get_all()
        if context:
            log_format += f" {context}"

        return log_format


# =============================================================
# Logger personnalisé
# =============================================================


class CustomLogger(logging.Logger):
    """Logger avec méthodes supplémentaires"""

    def log_with_context(self, level: int, msg: str, **kwargs):
        """Log avec contexte supplémentaire"""
        extra = {"extra_fields": kwargs}
        self.log(level, msg, extra=extra)

    def debug_dict(self, data: Dict, message: str = ""):
        """Log un dictionnaire en mode debug"""
        if message:
            self.debug(message)
        self.debug(json.dumps(data, indent=2, default=str))

    def info_dict(self, data: Dict, message: str = ""):
        """Log un dictionnaire en mode info"""
        if message:
            self.info(message)
        self.info(json.dumps(data, indent=2, default=str))

    def request(self, method: str, path: str, status: int, duration: float, **kwargs):
        """Log une requête HTTP"""
        self.log_with_context(
            logging.INFO,
            f"{method} {path} - {status}",
            method=method,
            path=path,
            status=status,
            duration_ms=round(duration * 1000, 2),
            **kwargs,
        )

    def query(self, sql: str, params: Optional[tuple] = None, duration: Optional[float] = None):
        """Log une requête SQL"""
        if log_config.log_sql_queries:
            extra = {
                "sql": sql,
                "params": params,
            }
            if duration:
                extra["duration_ms"] = round(duration * 1000, 2)

            self.log_with_context(logging.DEBUG, "SQL Query", **extra)

    def security(self, event: str, **kwargs):
        """Log un événement de sécurité"""
        self.log_with_context(
            logging.WARNING, f"Security Event: {event}", security_event=event, **kwargs
        )

    def performance(self, operation: str, duration: float, **kwargs):
        """Log une métrique de performance"""
        self.log_with_context(
            logging.INFO,
            f"Performance: {operation}",
            operation=operation,
            duration_ms=round(duration * 1000, 2),
            **kwargs,
        )


# =============================================================
# Configuration du système de logging
# =============================================================


def setup_logging(
    app_name: str = "microframework", config: Optional[LogConfig] = None
) -> CustomLogger:
    """
    Configure le système de logging

    Args:
        app_name: Nom de l'application
        config: Configuration personnalisée

    Returns:
        Logger configuré
    """
    global log_config

    if config:
        log_config = config

    # Créer le répertoire de logs
    if log_config.enable_file:
        log_config.log_dir.mkdir(exist_ok=True)

    # Enregistrer la classe de logger personnalisée
    logging.setLoggerClass(CustomLogger)

    # Créer le logger
    logger = logging.getLogger(app_name)
    logger.setLevel(log_config.log_level)

    # Supprimer les handlers existants
    logger.handlers.clear()

    # Handler console
    if log_config.enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_config.log_level)

        if log_config.log_format == "json":
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(ColoredFormatter())

        logger.addHandler(console_handler)

    # Handler fichier
    if log_config.enable_file:
        # Fichier principal
        log_file = log_config.log_dir / f"{app_name}.log"

        if log_config.enable_rotation:
            # Rotation par temps
            file_handler = TimedRotatingFileHandler(
                log_file, when=log_config.rotation_interval, backupCount=log_config.backup_count
            )
        else:
            # Rotation par taille
            file_handler = RotatingFileHandler(
                log_file, maxBytes=log_config.max_file_size, backupCount=log_config.backup_count
            )

        file_handler.setLevel(log_config.log_level)

        if log_config.log_format == "json":
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )

        logger.addHandler(file_handler)

        # Fichier d'erreurs séparé
        error_file = log_config.log_dir / f"{app_name}.error.log"
        error_handler = RotatingFileHandler(
            error_file, maxBytes=log_config.max_file_size, backupCount=log_config.backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        logger.addHandler(error_handler)

    # Ne pas propager aux loggers parents
    logger.propagate = False

    return logger


# =============================================================
# Décorateur de logging
# =============================================================


def log_execution(logger: Optional[logging.Logger] = None):
    """
    Décorateur pour logger l'exécution d'une fonction

    Usage:
        @log_execution()
        def my_function(x, y):
            return x + y
    """

    def decorator(func):
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__qualname__
            logger.debug(f"Executing {func_name}")

            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(
                    f"Completed {func_name}",
                    extra={"extra_fields": {"duration_ms": round(duration * 1000, 2)}},
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Failed {func_name}: {str(e)}",
                    exc_info=True,
                    extra={"extra_fields": {"duration_ms": round(duration * 1000, 2)}},
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__qualname__
            logger.debug(f"Executing {func_name}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(
                    f"Completed {func_name}",
                    extra={"extra_fields": {"duration_ms": round(duration * 1000, 2)}},
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Failed {func_name}: {str(e)}",
                    exc_info=True,
                    extra={"extra_fields": {"duration_ms": round(duration * 1000, 2)}},
                )
                raise

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
