from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import Synthesis


class SynthesisRepository:
    COLLECTION_NAME = 'syntheses'

    @staticmethod
    def create(synthesis: Synthesis) -> Synthesis:
        data = synthesis.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat()
        
        # Insert synthesis into MongoDB
        collection = mongodb_connector.get_collection(SynthesisRepository.COLLECTION_NAME)
        collection.insert_one(data)
        return synthesis

    @staticmethod
    def update(synthesis: Synthesis) -> Synthesis:
        data = synthesis.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat()
        
        # Update synthesis in MongoDB
        collection = mongodb_connector.get_collection(SynthesisRepository.COLLECTION_NAME)
        collection.update_one(
            {'id': synthesis.id},
            {'$set': data}
        )
        return synthesis

    @staticmethod
    def get_by_id(synthesis_id: str) -> Optional[Synthesis]:
        collection = mongodb_connector.get_collection(SynthesisRepository.COLLECTION_NAME)
        doc = collection.find_one({'id': synthesis_id})
        
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

    @staticmethod
    def list_all() -> List[Synthesis]:
        collection = mongodb_connector.get_collection(SynthesisRepository.COLLECTION_NAME)
        docs = collection.find()
        
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

    @staticmethod
    def delete(synthesis_id: str) -> None:
        collection = mongodb_connector.get_collection(SynthesisRepository.COLLECTION_NAME)
        collection.delete_one({'id': synthesis_id})


