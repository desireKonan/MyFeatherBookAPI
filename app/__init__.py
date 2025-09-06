"""
Feather Book API Application
"""

from flask import Flask
from flask_cors import CORS
from app.firebase_connector import initialize_firebase
from app.routes import health_bp, notes_bp, syntheses_bp
#from app.logger_config import setup_default_logging
#from app.middleware import LoggingMiddleware

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Setup logging first
    #setup_default_logging()
    
    # Enable CORS
    CORS(app)
    
    # Initialize Firebase
    initialize_firebase()
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(syntheses_bp)
    
    # Initialize logging middleware
    #LoggingMiddleware(app)
    
    # Register routes
    @app.route("/")
    def hello_world():
        return """
        <h1>Feather Book API</h1>
        <p>Bienvenue sur l'API Feather Book !</p>
        <p><a href="/api/v1/health">🏥 Health Check</a></p>
        <p><a href="/api/v1/notes">📝 Notes API</a></p>
        <p><a href="/api/v1/syntheses">📊 Syntheses API</a></p>
        """
    
    return app