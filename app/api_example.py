"""
Flask API example using Firebase models
"""

from flask import Flask, request, jsonify
from app.models import AttachmentType, Attachment, Note, Synthesis
from app.repository import NoteRepository, SynthesisRepository

app = Flask(__name__)

# Notes API endpoints
@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes"""
    try:
        notes = NoteRepository.list_all()
        return jsonify([note.to_dict() for note in notes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()
        note = Note(content=data.get('content', ''))
        
        # Add attachments if provided
        attachments_data = data.get('attachments', [])
        for att_data in attachments_data:
            attachment = Attachment(
                url=att_data.get('url'),
                type=AttachmentType(att_data.get('type'))
            )
            note.add_attachment(attachment)
        
        NoteRepository.create(note)
        return jsonify(note.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    try:
        note = NoteRepository.get_by_id(note_id)
        if note:
            return jsonify(note.to_dict()), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note"""
    try:
        note = Note.get_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        if 'content' in data:
            note.content = data['content']
        
        NoteRepository.update(note)
        return jsonify(note.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        NoteRepository.delete(note_id)
        return jsonify({'message': 'Note deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Synthesis API endpoints
@app.route('/api/syntheses', methods=['GET'])
def get_syntheses():
    """Get all syntheses"""
    try:
        syntheses = SynthesisRepository.list_all()
        return jsonify([synthesis.to_dict() for synthesis in syntheses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/syntheses', methods=['POST'])
def create_synthesis():
    """Create a new synthesis"""
    try:
        data = request.get_json()
        synthesis = Synthesis(
            url=data.get('url', ''),
            is_generated=data.get('is_generated', False)
        )
        SynthesisRepository.create(synthesis)
        return jsonify(synthesis.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/syntheses/<synthesis_id>', methods=['GET'])
def get_synthesis(synthesis_id):
    """Get a specific synthesis by ID"""
    try:
        synthesis = SynthesisRepository.get_by_id(synthesis_id)
        if synthesis:
            return jsonify(synthesis.to_dict()), 200
        else:
            return jsonify({'error': 'Synthesis not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/syntheses/<synthesis_id>', methods=['DELETE'])
def delete_synthesis(synthesis_id):
    """Delete a synthesis"""
    try:
        synthesis = SynthesisRepository.get_by_id(synthesis_id)
        if not synthesis:
            return jsonify({'error': 'Synthesis not found'}), 404
        
        SynthesisRepository.delete(synthesis_id)
        return jsonify({'message': 'Synthesis deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
