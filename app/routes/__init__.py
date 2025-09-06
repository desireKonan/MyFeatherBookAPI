"""
Package pour les routes de l'API
"""

from .health_routes import health_bp
from .notes_routes import notes_bp
from .syntheses_routes import syntheses_bp

__all__ = ['health_bp', 'notes_bp', 'syntheses_bp']
