"""
API principale pour Feather Book API
Configure et initialise tous les contrôleurs
"""

from flask_restx import Api
from app.controllers import notes_ns, syntheses_ns, health_ns

# Initialize Flask-RESTX API
api = Api(
    title='Feather Book API',
    version='1.0',
    description='API pour la gestion des notes, pièces jointes et synthèses avec Firebase',
    doc='/swagger/',
    prefix='/api/v1'
)

# Add namespaces to API
api.add_namespace(notes_ns)
api.add_namespace(syntheses_ns)
api.add_namespace(health_ns)
