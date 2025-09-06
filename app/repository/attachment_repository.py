from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import Attachment


class AttachmentRepository:
    COLLECTION_NAME = 'attachments'

    @staticmethod
    def create(attachment: Attachment) -> Attachment:
        data = attachment.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in data and data['created_at']:
            data['created_at'] = data['created_at'].isoformat()
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = data['updated_at'].isoformat()
        
        # Insert attachment into MongoDB
        collection = mongodb_connector.get_collection(AttachmentRepository.COLLECTION_NAME)
        result = collection.insert_one(data)
        return attachment

    @staticmethod
    def update(attachment: Attachment) -> Attachment:
        attachment_dict = attachment.to_dict()
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in attachment_dict and attachment_dict['created_at']:
            attachment_dict['created_at'] = attachment_dict['created_at'].isoformat()
        if 'updated_at' in attachment_dict and attachment_dict['updated_at']:
            attachment_dict['updated_at'] = attachment_dict['updated_at'].isoformat()
        
        # Update attachment in MongoDB
        collection = mongodb_connector.get_collection(AttachmentRepository.COLLECTION_NAME)
        collection.update_one(
            {'id': attachment.id},
            {'$set': attachment_dict}
        )
        return attachment

    @staticmethod
    def get_by_id(attachment_id: str) -> Optional[Attachment]:
        collection = mongodb_connector.get_collection(AttachmentRepository.COLLECTION_NAME)
        doc = collection.find_one({'id': attachment_id})
        
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
        
        return Attachment.from_dict(doc)

    @staticmethod
    def list_by_note(note_id: str) -> List[Attachment]:
        collection = mongodb_connector.get_collection(AttachmentRepository.COLLECTION_NAME)
        docs = collection.find({'note_id': note_id})
        
        attachments = []
        for doc in docs:
            # Convert ObjectId to string and handle datetime conversion
            doc['_id'] = str(doc['_id'])
            if 'created_at' in doc and isinstance(doc['created_at'], str):
                from datetime import datetime
                doc['created_at'] = datetime.fromisoformat(doc['created_at'].replace('Z', '+00:00'))
            if 'updated_at' in doc and isinstance(doc['updated_at'], str):
                from datetime import datetime
                doc['updated_at'] = datetime.fromisoformat(doc['updated_at'].replace('Z', '+00:00'))
            
            attachments.append(Attachment.from_dict(doc))
        
        return attachments

    @staticmethod
    def delete(attachment_id: str) -> None:
        collection = mongodb_connector.get_collection(AttachmentRepository.COLLECTION_NAME)
        collection.delete_one({'id': attachment_id})