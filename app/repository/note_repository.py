from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import Note


class NoteRepository:
    COLLECTION_NAME = 'notes'
    
    def __init__(self):
        self.collection = mongodb_connector.get_collection(self.COLLECTION_NAME)
    
    def create(self, note: Note) -> Note:
        """Créer une nouvelle note"""
        note_dict = note.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in note_dict and note_dict['created_at']:
            note_dict['created_at'] = note_dict['created_at'].isoformat()
        if 'updated_at' in note_dict and note_dict['updated_at']:
            note_dict['updated_at'] = note_dict['updated_at'].isoformat()
        
        # Insert note into MongoDB
        self.collection.insert_one(note_dict)
        
        return note

    def update(self, note: Note) -> Note:
        """Mettre à jour une note existante"""
        note_dict = note.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in note_dict and note_dict['created_at']:
            note_dict['created_at'] = note_dict['created_at'].isoformat()
        if 'updated_at' in note_dict and note_dict['updated_at']:
            note_dict['updated_at'] = note_dict['updated_at'].isoformat()
        
        # Update note in MongoDB
        self.collection.update_one(
            {'id': note.id},
            {'$set': note_dict}
        )
        
        return note

    def get_by_id(self, note_id: str) -> Optional[Note]:
        """Récupérer une note par son ID"""
        doc = self.collection.find_one({'id': note_id})
        
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
        
        return Note.from_dict(doc)

    def list_all(self) -> List[Note]:
        """Récupérer toutes les notes"""
        docs = self.collection.find()
        
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
            
            notes.append(Note.from_dict(doc))
        
        return notes

    def delete(self, note_id: str) -> bool:
        """Supprimer une note par son ID"""
        result = self.collection.delete_one({'id': note_id})
        return result.deleted_count > 0

    def exists(self, note_id: str) -> bool:
        """Vérifier si une note existe"""
        return self.collection.count_documents({'id': note_id}) > 0

    def count(self) -> int:
        """Compter le nombre total de notes"""
        return self.collection.count_documents({})