# =============================================================
# Middleware de logging des requêtes
# =============================================================
import logging
from .logger import CustomLogger, log_context
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import uuid


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware pour logger toutes les requêtes HTTP"""
    
    def __init__(self, app, logger: Optional[CustomLogger] = None):
        super().__init__(app)
        self.logger = logger or logging.getLogger("microframework")
    
    async def dispatch(self, request: Request, call_next):
        # Générer un ID de requête unique
        request_id = str(uuid.uuid4())
        
        # Ajouter au contexte
        log_context.set("request_id", request_id)
        log_context.set("method", request.method)
        log_context.set("path", request.url.path)
        log_context.set("client_ip", request.client.host)
        
        # Ajouter l'ID à la requête
        request.state.request_id = request_id
        
        # Logger le début de la requête
        start_time = time.time()
        
        self.logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                'extra_fields': {
                    'request_id': request_id,
                    'user_agent': request.headers.get('user-agent'),
                    'query_params': dict(request.query_params)
                }
            }
        )
        
        # Traiter la requête
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Logger la fin de la requête
            self.logger.request(
                method=request.method,
                path=request.url.path,
                status=response.status_code,
                duration=duration,
                request_id=request_id
            )
            
            # Ajouter l'ID de requête dans les headers de réponse
            response.headers["X-Request-ID"] = request_id
            
            return response
        
        except Exception as e:
            duration = time.time() - start_time
            
            # Logger l'erreur
            self.logger.error(
                f"Request failed: {request.method} {request.url.path}",
                exc_info=True,
                extra={
                    'extra_fields': {
                        'request_id': request_id,
                        'duration': duration,
                        'error': str(e)
                    }
                }
            )
            
            raise
        
        finally:
            # Nettoyer le contexte
            log_context.clear()
