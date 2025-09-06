"""
Routes pour les opérations sur les notes
"""

from flask import Blueprint, request, jsonify
from app.models import AttachmentType, Attachment, Note
from app.repository import NoteRepository
from app.logger_config import get_logger
from app.middleware import log_function_call

# Create blueprint for notes
notes_bp = Blueprint('notes', __name__, url_prefix='/api/v1/notes')



@notes_bp.route('', methods=['GET'])
@log_function_call('list_notes')
def list_notes():
    """Récupérer toutes les notes"""
    logger = get_logger('notes_routes')
    try:
        logger.info("Récupération de toutes les notes")
        notes = NoteRepository.list_all()
        logger.info(f"Récupération réussie: {len(notes)} notes trouvées")
        return jsonify([note.to_dict() for note in notes]), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des notes: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération des notes: {str(e)}"}), 500



@notes_bp.route('/<string:note_id>', methods=['GET'])
@log_function_call('get_note_by_id')
def get_note(note_id):
    """Récupérer une note par son ID"""
    logger = get_logger('notes_routes')
    try:
        logger.info(f"Récupération de la note avec ID: {note_id}")
        note = NoteRepository.get_by_id(note_id)
        if not note:
            logger.warning(f"Note non trouvée avec ID: {note_id}")
            return jsonify({'error': 'Note non trouvée'}), 404
        logger.info(f"Note récupérée avec succès: {note_id}")
        return jsonify(note.to_dict()), 200
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la note {note_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la récupération de la note: {str(e)}"}), 500



@notes_bp.route('', methods=['POST'])
@log_function_call('create_note')
def create_note():
    """Créer une nouvelle note"""
    logger = get_logger('notes_routes')
    try:
        data = request.get_json()
        logger.info(f"Création d'une nouvelle note avec {len(data.get('attachments', []))} pièces jointes")
        
        if not data or 'content' not in data:
            logger.warning("Tentative de création de note sans contenu")
            return jsonify({'error': 'Le contenu de la note est requis'}), 400
        
        note = Note(content=data['content'])
        
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
            
            attachment = Attachment(url=att_data['url'], type=attachment_type)
            note.add_attachment(attachment)
        
        NoteRepository.create(note)
        logger.info(f"Note créée avec succès, ID: {note.id}")
        return jsonify(note.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de la note: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la création de la note: {str(e)}"}), 500



@notes_bp.route('/<string:note_id>', methods=['PUT'])
@log_function_call('update_note')
def update_note(note_id):
    """Mettre à jour une note"""
    logger = get_logger('notes_routes')
    try:
        logger.info(f"Mise à jour de la note avec ID: {note_id}")
        note = NoteRepository.get_by_id(note_id)
        if not note:
            logger.warning(f"Note non trouvée pour mise à jour: {note_id}")
            return jsonify({'error': 'Note non trouvée'}), 404
        
        data = request.get_json()
        if data and 'content' in data:
            logger.info(f"Contenu de la note {note_id} mis à jour")
            note.content = data['content']
            NoteRepository.update(note)
        
        logger.info(f"Note {note_id} mise à jour avec succès")
        return jsonify(note.to_dict()), 200
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la note {note_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la mise à jour de la note: {str(e)}"}), 500



@notes_bp.route('/<string:note_id>', methods=['DELETE'])
@log_function_call('delete_note')
def delete_note(note_id):
    """Supprimer une note"""
    logger = get_logger('notes_routes')
    try:
        logger.info(f"Suppression de la note avec ID: {note_id}")
        note = NoteRepository.get_by_id(note_id)
        if not note:
            logger.warning(f"Note non trouvée pour suppression: {note_id}")
            return jsonify({'error': 'Note non trouvée'}), 404
        
        NoteRepository.delete(note_id)
        logger.info(f"Note {note_id} supprimée avec succès")
        return jsonify({'message': 'Note supprimée avec succès'}), 200
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la note {note_id}: {str(e)}", exc_info=True)
        return jsonify({'error': f"Erreur lors de la suppression de la note: {str(e)}"}), 500
