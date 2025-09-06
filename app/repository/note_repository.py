from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import Note, Attachment
from .attachment_repository import AttachmentRepository


class NoteRepository:
    COLLECTION_NAME = 'notes'

    @staticmethod
    def create(note: Note) -> Note:
        # Persist note
        note_dict = note.to_dict()
        print(f'Creating note: {note_dict}')
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in note_dict and note_dict['created_at']:
            note_dict['created_at'] = note_dict['created_at'].isoformat()
        if 'updated_at' in note_dict and note_dict['updated_at']:
            note_dict['updated_at'] = note_dict['updated_at'].isoformat()
        
        # Store attachment IDs separately
        attachment_ids = [att.id for att in note.attachments]
        note_dict['attachments'] = attachment_ids
        
        # Insert note into MongoDB
        collection = mongodb_connector.get_collection(NoteRepository.COLLECTION_NAME)
        collection.insert_one(note_dict)
        
        # Persist attachments with back-reference
        for attachment in note.attachments:
            attachment.note_id = note.id
            AttachmentRepository.create(attachment)
        
        return note

    @staticmethod
    def update(note: Note) -> Note:
        note_dict = note.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in note_dict and note_dict['created_at']:
            note_dict['created_at'] = note_dict['created_at'].isoformat()
        if 'updated_at' in note_dict and note_dict['updated_at']:
            note_dict['updated_at'] = note_dict['updated_at'].isoformat()
        
        # Store attachment IDs separately
        attachment_ids = [att.id for att in note.attachments]
        note_dict['attachments'] = attachment_ids
        
        # Update note in MongoDB
        collection = mongodb_connector.get_collection(NoteRepository.COLLECTION_NAME)
        collection.update_one(
            {'id': note.id},
            {'$set': note_dict}
        )

        # Ensure attachments exist and are linked
        for attachment in note.attachments:
            attachment.note_id = note.id
            AttachmentRepository.update(attachment)
        
        return note

    @staticmethod
    def get_by_id(note_id: str) -> Optional[Note]:
        collection = mongodb_connector.get_collection(NoteRepository.COLLECTION_NAME)
        doc = collection.find_one({'id': note_id})
        
        if not doc:
            return None
        
        # Convert ObjectId to string and handle datetime conversion
        doc['_id'] = str(doc['_id'])
        if 'created_at' in doc and isinstance(doc['created_at'], str):
            from datetime import datetime
            doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
        if 'updated_at' in doc and isinstance(doc['updated_at'], str):
            from datetime import datetime
            doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
        
        note = Note.from_dict(doc)
        # Load attachments by note_id
        note.attachments = AttachmentRepository.list_by_note(note.id)
        return note

    @staticmethod
    def list_all() -> List[Note]:
        collection = mongodb_connector.get_collection(NoteRepository.COLLECTION_NAME)
        docs = collection.find()
        
        notes: List[Note] = []
        for doc in docs:
            # Convert ObjectId to string and handle datetime conversion
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc and isinstance(doc['created_at'], str):
                from datetime import datetime
                doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
            if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                from datetime import datetime
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
            
            note = Note.from_dict(doc)
            note.attachments = AttachmentRepository.list_by_note(note.id)
            notes.append(note)
        
        return notes

    @staticmethod
    def delete(note_id: str) -> None:
        # Delete attachments first
        attachments = AttachmentRepository.list_by_note(note_id)
        for attachment in attachments:
            AttachmentRepository.delete(attachment.id)
        
        # Delete note from MongoDB
        collection = mongodb_connector.get_collection(NoteRepository.COLLECTION_NAME)
        collection.delete_one({'id': note_id})


