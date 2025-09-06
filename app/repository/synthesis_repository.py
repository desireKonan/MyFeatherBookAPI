from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import Synthesis, Attachment, AttachmentType


class SynthesisRepository:
    COLLECTION_NAME = 'syntheses'
    
    def __init__(self):
        self.collection = mongodb_connector.get_collection(self.COLLECTION_NAME)

    def create(self, synthesis: Synthesis) -> Synthesis:
        """Créer une nouvelle synthèse"""
        data = synthesis.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat()
        
        # Insert synthesis into MongoDB (attachments are embedded)
        self.collection.insert_one(data)
        return synthesis

    def update(self, synthesis: Synthesis) -> Synthesis:
        """Mettre à jour une synthèse existante"""
        data = synthesis.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat()
        
        # Update synthesis in MongoDB
        self.collection.update_one(
            {'id': synthesis.id},
            {'$set': data}
        )
        return synthesis

    def get_by_id(self, synthesis_id: str) -> Optional[Synthesis]:
        """Récupérer une synthèse par son ID"""
        doc = self.collection.find_one({'id': synthesis_id})
        
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
        
        return Synthesis.from_dict(doc)

    def list_all(self) -> List[Synthesis]:
        """Récupérer toutes les synthèses"""
        docs = self.collection.find()
        
        syntheses = []
        for doc in docs:
            # Convert ObjectId to string and handle datetime conversion
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc and isinstance(doc['created_at'], str):
                from datetime import datetime
                doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
            if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                from datetime import datetime
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
            
            syntheses.append(Synthesis.from_dict(doc))
        
        return syntheses

    def list_by_note(self, note_id: str) -> List[Synthesis]:
        """Récupérer toutes les synthèses d'une note"""
        docs = self.collection.find({'note_id': note_id})
        
        syntheses = []
        for doc in docs:
            # Convert ObjectId to string and handle datetime conversion
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc and isinstance(doc['created_at'], str):
                from datetime import datetime
                doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
            if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                from datetime import datetime
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
            
            syntheses.append(Synthesis.from_dict(doc))
        
        return syntheses

    def delete(self, synthesis_id: str) -> bool:
        """Supprimer une synthèse par son ID"""
        result = self.collection.delete_one({'id': synthesis_id})
        return result.deleted_count > 0

    def exists(self, synthesis_id: str) -> bool:
        """Vérifier si une synthèse existe"""
        return self.collection.count_documents({'id': synthesis_id}) > 0

    def count(self) -> int:
        """Compter le nombre total de synthèses"""
        return self.collection.count_documents({})

    def count_by_note(self, note_id: str) -> int:
        """Compter le nombre de synthèses pour une note"""
        return self.collection.count_documents({'note_id': note_id})

    def add_attachment_to_synthesis(self, synthesis_id: str, url: str, attachment_type: AttachmentType, name: str = "", size: int = 0) -> Optional[Synthesis]:
        """Ajouter un attachment à une synthèse"""
        synthesis = self.get_by_id(synthesis_id)
        if not synthesis:
            return None
        
        synthesis.add_attachment(url, attachment_type, name, size)
        return self.update(synthesis)

    def remove_attachment_from_synthesis(self, synthesis_id: str, url: str) -> Optional[Synthesis]:
        """Supprimer un attachment d'une synthèse"""
        synthesis = self.get_by_id(synthesis_id)
        if not synthesis:
            return None
        
        synthesis.remove_attachment(url)
        return self.update(synthesis)

    def get_attachments_by_type(self, synthesis_id: str, attachment_type: AttachmentType) -> List[Attachment]:
        """Récupérer les attachments d'une synthèse par type"""
        synthesis = self.get_by_id(synthesis_id)
        if not synthesis:
            return []
        
        return synthesis.get_attachments_by_type(attachment_type)

    def search_by_title(self, title: str) -> List[Synthesis]:
        """Rechercher des synthèses par titre"""
        docs = self.collection.find({'title': {'$regex': title, '$options': 'i'}})
        
        syntheses = []
        for doc in docs:
            # Convert ObjectId to string and handle datetime conversion
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc and isinstance(doc['created_at'], str):
                from datetime import datetime
                doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
            if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                from datetime import datetime
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
            
            syntheses.append(Synthesis.from_dict(doc))
        
        return syntheses