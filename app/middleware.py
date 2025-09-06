"""
Middleware Flask pour le logging automatique et la gestion des erreurs
"""

import time
import functools
import logging
from flask import request, g
from app.logger_config import log_request, log_error, log_performance, get_logger

logger = get_logger('middleware')

class LoggingMiddleware:
    """Middleware pour logger automatiquement les requêtes HTTP"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger('middleware')
        
        # Enregistrer les hooks
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)
        app.errorhandler(Exception)(self.handle_exception)
    
    def before_request(self):
        """Exécuté avant chaque requête"""
        # Marquer le début de la requête
        g.start_time = time.time()
        g.request_id = f"req_{int(time.time() * 1000)}"
        
        # Logger le début de la requête
        self.logger.debug(
            f"Request started: {request.method} {request.url}",
            extra={
                'request_id': g.request_id,
                'method': request.method,
                'url': request.url,
                'remote_addr': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', 'Unknown')
            }
        )
        # Logger les paramètres de la requête pour le debug
        if self.logger.isEnabledFor(logging.DEBUG):
            if request.args:
                self.logger.debug(f"Query parameters: {dict(request.args)}")
            if request.json:
                self.logger.debug(f"Request body: {request.json}")
                
        if request.method != 'GET' and request.content_type == 'application/json':
            try:
                if request.get_data():  # Vérifier s'il y a des données
                    request.json = request.get_json()
            except Exception as e:
                self.logger.warning(f"Failed to parse JSON: {e}")


    def after_request(self, response):
        """Exécuté après chaque requête"""
        # Calculer la durée de la requête
        duration = time.time() - g.start_time
        
        # Logger la requête complète
        log_request(request, response, duration)
        
        # Logger les performances
        log_performance(
            f"{request.method} {request.url}",
            duration,
            {
                'request_id': g.request_id,
                'status_code': response.status_code,
                'content_length': response.content_length
            }
        )
        
        # Logger la fin de la requête
        self.logger.debug(
            f"Request completed: {request.method} {request.url} - {response.status_code} in {duration:.3f}s",
            extra={
                'request_id': g.request_id,
                'duration': duration,
                'status_code': response.status_code
            }
        )
        
        return response
    
    def teardown_request(self, exception=None):
        """Exécuté après le traitement de la requête, même en cas d'erreur"""
        if exception:
            self.logger.error(
                f"Request failed: {request.method} {request.url}",
                exc_info=True,
                extra={
                    'request_id': g.request_id,
                    'method': request.method,
                    'url': request.url
                }
            )
    
    def handle_exception(self, exception):
        """Gestionnaire d'erreurs global"""
        # Logger l'erreur avec contexte
        log_error(exception, {
            'request_id': g.request_id,
            'method': request.method,
            'url': request.url,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown')
        })
        
        # Re-raise l'exception pour que Flask la gère normalement
        raise exception

def log_function_call(func_name=None):
    """
    Décorateur pour logger les appels de fonction avec mesure de performance
    
    Args:
        func_name (str): Nom personnalisé pour la fonction (optionnel)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            
            try:
                logger.debug(f"Function call started: {name}")
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.debug(f"Function call completed: {name} in {duration:.3f}s")
                log_performance(name, duration)
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Function call failed: {name} after {duration:.3f}s", exc_info=True)
                log_error(e, {'function': name, 'duration': duration})
                raise
        
        return wrapper
    return decorator

def log_database_operation(operation_type):
    """
    Décorateur pour logger les opérations de base de données
    
    Args:
        operation_type (str): Type d'opération (CREATE, READ, UPDATE, DELETE)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = f"DB_{operation_type}_{func.__name__}"
            start_time = time.time()
            
            try:
                logger.debug(f"Database operation started: {name}")
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.debug(f"Database operation completed: {name} in {duration:.3f}s")
                log_performance(name, duration, {
                    'operation_type': operation_type,
                    'function': func.__name__
                })
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Database operation failed: {name} after {duration:.3f}s", exc_info=True)
                log_error(e, {
                    'operation_type': operation_type,
                    'function': func.__name__,
                    'duration': duration
                })
                raise
        
        return wrapper
    return decorator

# Décorateurs spécifiques pour les opérations CRUD
log_create = lambda func: log_database_operation('CREATE')(func)
log_read = lambda func: log_database_operation('READ')(func)
log_update = lambda func: log_database_operation('UPDATE')(func)
log_delete = lambda func: log_database_operation('DELETE')(func)
