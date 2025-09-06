"""
Routes pour les opérations sur les synthèses
"""

from flask import Blueprint, request, jsonify
from app.models import Synthesis, AttachmentType
from app.repository import repository_factory
from app.logger_config import get_logger
from app.middleware import log_function_call

# Create blueprint for syntheses
syntheses_bp = Blueprint('syntheses', __name__, url_prefix='/api/v1/syntheses')

# Get repository instance
synthesis_repository = repository_factory.synthesis_repository


@syntheses_bp.route('', methods=['GET'])
@log_function_call('list_syntheses')
def list_syntheses():
    """Récupérer toutes les synthèses"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info("Récupération de toutes les synthèses")
        syntheses = synthesis_repository.list_all()
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
            is_generated=data.get('is_generated', False),
            note_id=data.get('note_id'),
            title=data.get('title', '')
        )
        
        # Ajouter les pièces jointes si fournies
        attachments_data = data.get('attachments', [])
        for att_data in attachments_data:
            if 'url' not in att_data or 'type' not in att_data:
                logger.warning(f"Pièce jointe invalide: {att_data}")
                return jsonify({'error': 'URL et type requis pour chaque pièce jointe'}), 400
            
            try:
                attachment_type = AttachmentType(att_data['type'])
            except ValueError:
                logger.warning(f"Type de pièce jointe invalide: {att_data['type']}")
                return jsonify({'error': f"Type de pièce jointe invalide: {att_data['type']}"}), 400
            
            synthesis.add_attachment(
                url=att_data['url'],
                attachment_type=attachment_type,
                name=att_data.get('name', ''),
                size=att_data.get('size', 0)
            )
        
        synthesis_repository.create(synthesis)
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
        synthesis = synthesis_repository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée avec ID: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        logger.info(f"Synthèse récupérée avec succès: {synthesis_id}")
        return jsonify(synthesis.to_dict()), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération de la synthèse: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>', methods=['PUT'])
@log_function_call('update_synthesis')
def update_synthesis(synthesis_id):
    """Mettre à jour une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Mise à jour de la synthèse avec ID: {synthesis_id}")
        synthesis = synthesis_repository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée pour mise à jour: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
        data = request.get_json()
        if data:
            if 'url' in data:
                synthesis.url = data['url']
            if 'is_generated' in data:
                synthesis.is_generated = data['is_generated']
            if 'note_id' in data:
                synthesis.note_id = data['note_id']
            if 'title' in data:
                synthesis.title = data['title']
            
            synthesis_repository.update(synthesis)
        
        logger.info(f"Synthèse {synthesis_id} mise à jour avec succès")
        return jsonify(synthesis.to_dict()), 200
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la mise à jour de la synthèse: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>', methods=['DELETE'])
@log_function_call('delete_synthesis')
def delete_synthesis(synthesis_id):
    """Supprimer une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Suppression de la synthèse avec ID: {synthesis_id}")
        if not synthesis_repository.exists(synthesis_id):
            logger.warning(f"Synthèse non trouvée pour suppression: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
        success = synthesis_repository.delete(synthesis_id)
        if success:
            logger.info(f"Synthèse {synthesis_id} supprimée avec succès")
            return jsonify({'message': 'Synthèse supprimée avec succès'}), 200
        else:
            logger.error(f"Échec de la suppression de la synthèse {synthesis_id}")
            return jsonify({'error': 'Échec de la suppression de la synthèse'}), 500
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la suppression de la synthèse: {str(e)}"}), 500


@syntheses_bp.route('/search', methods=['GET'])
@log_function_call('search_syntheses')
def search_syntheses():
    """Rechercher des synthèses par titre"""
    logger = get_logger('syntheses_routes')
    try:
        title = request.args.get('title', '')
        if not title:
            logger.warning("Recherche de synthèses sans terme de recherche")
            return jsonify({'error': 'Le paramètre title est requis pour la recherche'}), 400
        
        logger.info(f"Recherche de synthèses avec le titre: {title}")
        syntheses = synthesis_repository.search_by_title(title)
        logger.info(f"Recherche réussie: {len(syntheses)} synthèses trouvées")
        return jsonify([synthesis.to_dict() for synthesis in syntheses]), 200
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de synthèses: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la recherche de synthèses: {str(e)}"}), 500


@syntheses_bp.route('/note/<string:note_id>', methods=['GET'])
@log_function_call('get_syntheses_by_note')
def get_syntheses_by_note(note_id):
    """Récupérer toutes les synthèses d'une note"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Récupération des synthèses pour la note: {note_id}")
        syntheses = synthesis_repository.list_by_note(note_id)
        logger.info(f"Récupération réussie: {len(syntheses)} synthèses trouvées pour la note {note_id}")
        return jsonify([synthesis.to_dict() for synthesis in syntheses]), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des synthèses pour la note {note_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des synthèses: {str(e)}"}), 500


@syntheses_bp.route('/stats', methods=['GET'])
@log_function_call('get_synthesis_stats')
def get_synthesis_stats():
    """Récupérer les statistiques des synthèses"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info("Récupération des statistiques des synthèses")
        
        total_count = synthesis_repository.count()
        
        # Statistiques par type de génération
        all_syntheses = synthesis_repository.list_all()
        generated_count = sum(1 for s in all_syntheses if s.is_generated)
        manual_count = total_count - generated_count
        
        # Statistiques des attachments
        total_attachments = sum(len(s.attachments) for s in all_syntheses)
        audio_attachments = sum(len(s.get_attachments_by_type(AttachmentType.AUDIO)) for s in all_syntheses)
        document_attachments = sum(len(s.get_attachments_by_type(AttachmentType.DOCUMENT)) for s in all_syntheses)
        
        stats = {
            'total_syntheses': total_count,
            'generated_syntheses': generated_count,
            'manual_syntheses': manual_count,
            'total_attachments': total_attachments,
            'audio_attachments': audio_attachments,
            'document_attachments': document_attachments
        }
        
        logger.info(f"Statistiques récupérées: {stats}")
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des statistiques: {str(e)}"}), 500


# Routes pour les attachments des synthèses
@syntheses_bp.route('/<string:synthesis_id>/attachments', methods=['GET'])
@log_function_call('get_synthesis_attachments')
def get_synthesis_attachments(synthesis_id):
    """Récupérer tous les attachments d'une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Récupération des attachments de la synthèse: {synthesis_id}")
        synthesis = synthesis_repository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
        attachments = [attachment.to_dict() for attachment in synthesis.attachments]
        logger.info(f"Récupération réussie: {len(attachments)} attachments trouvés")
        return jsonify(attachments), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des attachments de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des attachments: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>/attachments', methods=['POST'])
@log_function_call('add_attachment_to_synthesis')
def add_attachment_to_synthesis(synthesis_id):
    """Ajouter un attachment à une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        data = request.get_json()
        logger.info(f"Ajout d'un attachment à la synthèse: {synthesis_id}")
        
        if not data or 'url' not in data or 'type' not in data:
            logger.warning("URL et type requis pour l'attachment")
            return jsonify({'error': 'URL et type requis pour l\'attachment'}), 400
        
        try:
            attachment_type = AttachmentType(data['type'])
        except ValueError:
            logger.warning(f"Type d'attachment invalide: {data['type']}")
            return jsonify({'error': f"Type d'attachment invalide: {data['type']}"}), 400
        
        synthesis = synthesis_repository.add_attachment_to_synthesis(
            synthesis_id=synthesis_id,
            url=data['url'],
            attachment_type=attachment_type,
            name=data.get('name', ''),
            size=data.get('size', 0)
        )
        
        if synthesis:
            logger.info(f"Attachment ajouté avec succès à la synthèse {synthesis_id}")
            return jsonify(synthesis.to_dict()), 200
        else:
            logger.warning(f"Synthèse non trouvée: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout de l'attachment à la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de l'ajout de l'attachment: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>/attachments/<path:url>', methods=['DELETE'])
@log_function_call('remove_attachment_from_synthesis')
def remove_attachment_from_synthesis(synthesis_id, url):
    """Supprimer un attachment d'une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Suppression de l'attachment {url} de la synthèse: {synthesis_id}")
        
        synthesis = synthesis_repository.remove_attachment_from_synthesis(synthesis_id, url)
        
        if synthesis:
            logger.info(f"Attachment supprimé avec succès de la synthèse {synthesis_id}")
            return jsonify(synthesis.to_dict()), 200
        else:
            logger.warning(f"Synthèse ou attachment non trouvé: {synthesis_id}, {url}")
            return jsonify({'error': 'Synthèse ou attachment non trouvé'}), 404
        
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'attachment de la synthèse {synthesis_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la suppression de l'attachment: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>/attachments/by-type/<string:attachment_type>', methods=['GET'])
@log_function_call('get_attachments_by_type')
def get_attachments_by_type(synthesis_id, attachment_type):
    """Récupérer les attachments d'une synthèse par type"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Récupération des attachments de type {attachment_type} pour la synthèse: {synthesis_id}")
        
        try:
            attachment_type_enum = AttachmentType(attachment_type)
        except ValueError:
            logger.warning(f"Type d'attachment invalide: {attachment_type}")
            return jsonify({'error': f"Type d'attachment invalide: {attachment_type}"}), 400
        
        attachments = synthesis_repository.get_attachments_by_type(synthesis_id, attachment_type_enum)
        attachments_dict = [attachment.to_dict() for attachment in attachments]
        
        logger.info(f"Récupération réussie: {len(attachments_dict)} attachments de type {attachment_type} trouvés")
        return jsonify(attachments_dict), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des attachments par type: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des attachments: {str(e)}"}), 500


@syntheses_bp.route('/<string:synthesis_id>/attachments/count', methods=['GET'])
@log_function_call('get_attachment_count')
def get_attachment_count(synthesis_id):
    """Récupérer le nombre d'attachments d'une synthèse"""
    logger = get_logger('syntheses_routes')
    try:
        logger.info(f"Récupération du nombre d'attachments pour la synthèse: {synthesis_id}")
        synthesis = synthesis_repository.get_by_id(synthesis_id)
        if not synthesis:
            logger.warning(f"Synthèse non trouvée: {synthesis_id}")
            return jsonify({'error': 'Synthèse non trouvée'}), 404
        
        count = len(synthesis.attachments)
        logger.info(f"Nombre d'attachments récupéré: {count}")
        return jsonify({'attachment_count': count}), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du nombre d'attachments: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération du nombre d'attachments: {str(e)}"}), 500