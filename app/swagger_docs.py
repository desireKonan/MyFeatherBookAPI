"""
Configuration Swagger pour l'API avec Flask-APISPEC
"""

from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from marshmallow import Schema, fields

# Schemas pour la documentation
class AttachmentSchema(Schema):
    id = fields.Str(dump_only=True, description='ID unique de la pièce jointe')
    url = fields.Str(required=True, description='URL de la pièce jointe')
    type = fields.Str(enum=['AUDIO', 'DOCUMENT', 'IMAGE'], required=True, description='Type de pièce jointe')
    created_at = fields.DateTime(dump_only=True, description='Date de création')
    updated_at = fields.DateTime(dump_only=True, description='Date de mise à jour')

class NoteSchema(Schema):
    id = fields.Str(dump_only=True, description='ID unique de la note')
    content = fields.Str(required=True, description='Contenu de la note')
    attachments = fields.List(fields.Nested(AttachmentSchema), description='Liste des pièces jointes')
    created_at = fields.DateTime(dump_only=True, description='Date de création')
    updated_at = fields.DateTime(dump_only=True, description='Date de mise à jour')

class NoteCreateSchema(Schema):
    content = fields.Str(required=True, description='Contenu de la note')
    attachments = fields.List(fields.Nested(AttachmentSchema), description='Liste des pièces jointes à ajouter')

class NoteUpdateSchema(Schema):
    content = fields.Str(description='Nouveau contenu de la note')

class SynthesisSchema(Schema):
    id = fields.Str(dump_only=True, description='ID unique de la synthèse')
    url = fields.Str(required=True, description='URL de la synthèse')
    is_generated = fields.Bool(description='Indique si la synthèse a été générée automatiquement')
    created_at = fields.DateTime(dump_only=True, description='Date de création')
    updated_at = fields.DateTime(dump_only=True, description='Date de mise à jour')

class SynthesisCreateSchema(Schema):
    url = fields.Str(required=True, description='URL de la synthèse')
    is_generated = fields.Bool(description='Indique si la synthèse a été générée automatiquement')

class HealthSchema(Schema):
    status = fields.Str(description='Statut de l\'API')
    message = fields.Str(description='Message de statut')
    version = fields.Str(description='Version de l\'API')

class ErrorSchema(Schema):
    error = fields.Str(description='Message d\'erreur')
    code = fields.Int(description='Code d\'erreur HTTP')

def init_swagger(app: Flask):
    """Initialiser la documentation Swagger"""
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Feather Book API',
            version='1.0',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })
    
    docs = FlaskApiSpec(app)
    
    # Enregistrer les routes pour la documentation
    with app.test_request_context():
        # Health routes
        docs.register_existing_resources()
        
        # Notes routes
        docs.register_existing_resources()
        
        # Syntheses routes
        docs.register_existing_resources()
    
    return docs
