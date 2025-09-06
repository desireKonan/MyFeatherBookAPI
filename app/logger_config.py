"""
Configuration du système de logging pour Feather Book API
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Configuration des niveaux de logging
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Configuration des formats de logging
LOG_FORMATS = {
    'detailed': logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    ),
    'simple': logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s'
    ),
    'json': logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "logger": "%(name)s", "file": "%(filename)s:%(lineno)d", "function": "%(funcName)s"}'
    )
}

class CustomFormatter(logging.Formatter):
    """Formateur personnalisé avec couleurs pour la console"""
    
    # Codes de couleur ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Vert
        'WARNING': '\033[33m',    # Jaune
        'ERROR': '\033[31m',      # Rouge
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Ajouter la couleur au niveau de log
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logger(
    name='feather_book_api',
    level='INFO',
    log_to_file=True,
    log_to_console=True,
    log_format='detailed',
    max_file_size=10*1024*1024,  # 10MB
    backup_count=5
):
    """
    Configure le logger principal de l'application
    
    Args:
        name (str): Nom du logger
        level (str): Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file (bool): Activer la journalisation dans des fichiers
        log_to_console (bool): Activer la journalisation dans la console
        log_format (str): Format des logs (detailed, simple, json)
        max_file_size (int): Taille maximale des fichiers de log en bytes
        backup_count (int): Nombre de fichiers de sauvegarde à conserver
    """
    
    # Créer le logger principal
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))
    
    # Éviter la duplication des handlers
    if logger.handlers:
        return logger
    
    # Créer le dossier de logs s'il n'existe pas
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Formatter
    formatter = LOG_FORMATS.get(log_format, LOG_FORMATS['detailed'])
    
    # Handler pour la console
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))
        
        # Utiliser le formateur coloré pour la console
        console_formatter = CustomFormatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Handler pour les fichiers
    if log_to_file:
        # Log principal avec rotation
        main_log_file = log_dir / 'feather_book_api.log'
        file_handler = logging.handlers.RotatingFileHandler(
            main_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_LEVELS.get(level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Log des erreurs séparé
        error_log_file = log_dir / 'feather_book_api_errors.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        # Log des requêtes HTTP
        access_log_file = log_dir / 'feather_book_api_access.log'
        access_handler = logging.handlers.RotatingFileHandler(
            access_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(formatter)
        
        # Créer un logger séparé pour les accès
        access_logger = logging.getLogger(f'{name}.access')
        access_logger.setLevel(logging.INFO)
        access_logger.addHandler(access_handler)
        access_logger.propagate = False
    
    return logger

def get_logger(name=None):
    """
    Récupère un logger configuré
    
    Args:
        name (str): Nom du logger (optionnel)
    
    Returns:
        logging.Logger: Logger configuré
    """
    if name:
        return logging.getLogger(f'feather_book_api.{name}')
    return logging.getLogger('feather_book_api')

def log_request(request, response=None, duration=None):
    """
    Log une requête HTTP
    
    Args:
        request: Objet request Flask
        response: Objet response Flask (optionnel)
        duration (float): Durée de la requête en secondes (optionnel)
    """
    access_logger = logging.getLogger('feather_book_api.access')
    
    # Informations de base de la requête
    log_data = {
        'method': request.method,
        'url': request.url,
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Ajouter la durée si disponible
    if duration is not None:
        log_data['duration'] = f"{duration:.3f}s"
    
    # Ajouter le code de statut de la réponse si disponible
    if response:
        log_data['status_code'] = response.status_code
        log_data['status'] = response.status
    
    # Formater le message de log
    message = f"HTTP {log_data['method']} {log_data['url']} - {log_data.get('status_code', 'N/A')}"
    if duration:
        message += f" - {duration:.3f}s"
    
    # Log avec le niveau approprié
    if response and response.status_code >= 400:
        access_logger.warning(message, extra=log_data)
    else:
        access_logger.info(message, extra=log_data)

def log_error(error, context=None):
    """
    Log une erreur avec contexte
    
    Args:
        error: Exception ou message d'erreur
        context (dict): Contexte supplémentaire (optionnel)
    """
    logger = get_logger('errors')
    
    if isinstance(error, Exception):
        error_msg = f"{type(error).__name__}: {str(error)}"
        logger.error(error_msg, exc_info=True, extra=context or {})
    else:
        logger.error(str(error), extra=context or {})

def log_performance(operation, duration, details=None):
    """
    Log les performances d'une opération
    
    Args:
        operation (str): Nom de l'opération
        duration (float): Durée en secondes
        details (dict): Détails supplémentaires (optionnel)
    """
    logger = get_logger('performance')
    
    message = f"Performance: {operation} took {duration:.3f}s"
    logger.info(message, extra={
        'operation': operation,
        'duration': duration,
        'details': details or {}
    })

# Configuration par défaut
def setup_default_logging():
    """Configure le logging par défaut basé sur l'environnement"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        setup_logger(
            level='WARNING',
            log_to_file=True,
            log_to_console=False,
            log_format='json'
        )
    elif env == 'testing':
        setup_logger(
            level='DEBUG',
            log_to_file=False,
            log_to_console=True,
            log_format='simple'
        )
    else:  # development
        setup_logger(
            level='DEBUG',
            log_to_file=True,
            log_to_console=True,
            log_format='detailed'
        )
