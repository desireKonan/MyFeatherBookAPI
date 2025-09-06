"""
Configuration de l'application Feather Book API
"""

import os
from pathlib import Path

class Config:
    """Configuration de base"""
    
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Configuration du logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE', 'true').lower() == 'true'
    LOG_TO_CONSOLE = os.environ.get('LOG_TO_CONSOLE', 'true').lower() == 'true'
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'detailed')
    LOG_MAX_FILE_SIZE = int(os.environ.get('LOG_MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 5))
    
    # Configuration Firebase
    FIREBASE_SERVICE_ACCOUNT_KEY = os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY', 'serviceAccountKey.json')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Configuration de l'API
    API_TITLE = 'Feather Book API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'API pour la gestion des notes, pièces jointes et synthèses avec Firebase'
    
    # Configuration des dossiers
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / 'logs'
    UPLOADS_DIR = BASE_DIR / 'uploads'
    
    @classmethod
    def init_app(cls, app):
        """Initialiser la configuration de l'application"""
        # Créer les dossiers nécessaires
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.UPLOADS_DIR.mkdir(exist_ok=True)
        
        # Configuration spécifique à l'environnement
        if cls.FLASK_ENV == 'production':
            cls.init_production_config(app)
        elif cls.FLASK_ENV == 'testing':
            cls.init_testing_config(app)
        else:
            cls.init_development_config(app)
    
    @classmethod
    def init_development_config(cls, app):
        """Configuration pour le développement"""
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        
        # Logging détaillé en développement
        cls.LOG_LEVEL = 'DEBUG'
        cls.LOG_FORMAT = 'detailed'
        cls.LOG_TO_FILE = True
        cls.LOG_TO_CONSOLE = True
    
    @classmethod
    def init_production_config(cls, app):
        """Configuration pour la production"""
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        # Logging JSON en production
        cls.LOG_LEVEL = 'WARNING'
        cls.LOG_FORMAT = 'json'
        cls.LOG_TO_FILE = True
        cls.LOG_TO_CONSOLE = False
        
        # Sécurité en production
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production")
    
    @classmethod
    def init_testing_config(cls, app):
        """Configuration pour les tests"""
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        
        # Logging simple pour les tests
        cls.LOG_LEVEL = 'DEBUG'
        cls.LOG_FORMAT = 'simple'
        cls.LOG_TO_FILE = False
        cls.LOG_TO_CONSOLE = True

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = 'detailed'

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    LOG_FORMAT = 'json'
    LOG_TO_CONSOLE = False

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = 'simple'
    LOG_TO_FILE = False

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
