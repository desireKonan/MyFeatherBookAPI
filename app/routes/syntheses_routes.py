"""
Routes pour les opérations sur les synthèses
"""

from flask import Blueprint, request, jsonify
from app.models import Synthesis
from app.repository import SynthesisRepository
from app.logger_config import get_logger
from app.middleware import log_function_call

# Create blueprint for syntheses
syntheses_bp = Blueprint('syntheses', __name__, url_prefix='/api/v1/syntheses')

@syntheses_bp.route('', methods=['GET'])
@log_function_call('list_syntheses')
def list_syntheses():
    """Récupérer toutes les synthèses"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info("Récupération de toutes les synthèses")
        syntheses = SynthesisRepository.list_all()
        logger.info(f"Récupération réussie: {len(syntheses)} synthèses trouvées")
        return jsonify([synthesis.to_dict() for synthesis in syntheses]), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des synthèses: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des synthèses: {str(e)}"}), 500

@syntheses_bp.route('', methods=['POST'])
@log_function_call('create_synthesis')
def create_synthesis():
    """Créer une nouvelle synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        data = request.get_json()
        logger.info(f"Création d'une nouvelle synthèse: {data.get('url', 'N/A')}")
        
        if not data or 'url' not in data:
            logger.warning("Tentative de création de synthèse sans URL")
            return jsonify({'error': "L'URL de la synthèse est requise"}), 400
        
        synthesis = Synthesis(
            url=data['url'],
            is_generated=data.get('is_generated', False)
        )
        
        SynthesisRepository.create(synthesis)
        logger.info(f"Synthèse créée avec succès, ID: {synthesis.id}")
        return jsonify(synthesis.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de la synthèse: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la création de la synthèse: {str(e)}"}), 500

@syntheses_bp.route('/<string:synthesis_id>', methods=['GET'])
@log_function_call('get_synthesis_by_id')
def get_synthesis(synthesis_id):
    """Récupérer une synthèse par son ID"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Récupération de la synthèse avec ID: {synthesis_id}")
        synthesis = SynthesisRepository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée avec ID: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        logger.info(f"Synthèse récupérée avec succès: {synthesis_id}")
        return jsonify(synthesis.to_dict()), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération de la synthèse: {str(e)}"}), 500

@syntheses_bp.route('/<string:synthesis_id>', methods=['DELETE'])
@log_function_call('delete_synthesis')
def delete_synthesis(synthesis_id):
    """Supprimer une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Suppression de la synthèse avec ID: {synthesis_id}")
        synthesis = SynthesisRepository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée pour suppression: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
        SynthesisRepository.delete(synthesis_id)
        logger.info(f"Synthèse {synthesis_id} supprimée avec succès")
        return jsonify({'message': 'Synthèse supprimée avec succès'}), 200
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la suppression de la synthèse: {str(e)}"}), 500
