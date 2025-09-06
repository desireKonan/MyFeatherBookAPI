"""
Routes pour le health check de l'API
"""

from flask import Blueprint, jsonify
from app.logger_config import get_logger
from app.middleware import log_function_call

# Create blueprint for health check
health_bp = Blueprint('health', __name__, url_prefix='/api/v1/health')

@health_bp.route('', methods=['GET'])
@log_function_call('health_check')
def health_check():
    """Vérifier l'état de l'API"""
    logger = get_logger('health_check')
    logger.info("Health check demandé")
    
    return jsonify({
        'status': 'healthy',
        'message': 'Feather Book API is running',
        'version': '1.0'
    }), 200
