# app/repository/user_repository.py
from typing import List, Optional
from app.mongodb_connector import mongodb_connector
from app.models.model import User

class UserRepository:
    COLLECTION_NAME = 'users'
    
    def __init__(self):
        self.collection = mongodb_connector.get_collection(self.COLLECTION_NAME)
        # Créer un index unique sur username et email
        self.collection.create_index("username", unique=True)
        self.collection.create_index("email", unique=True)
    
    def create(self, user: User) -> User:
        """Créer un nouvel utilisateur"""
        user_dict = user.to_dict()
        user_dict['password_hash'] = user.password_hash
        
        # Convert datetime objects to ISO format for MongoDB
        if 'created_at' in user_dict and user_dict['created_at']:
            user_dict['created_at'] = user_dict['created_at'].isoformat()
        if 'updated_at' in user_dict and user_dict['updated_at']:
            user_dict['updated_at'] = user_dict['updated_at'].isoformat()
        if 'last_login' in user_dict and user_dict['last_login']:
            user_dict['last_login'] = user_dict['last_login'].isoformat()
        
        self.collection.insert_one(user_dict)
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Récupérer un utilisateur par ID"""
        doc = self.collection.find_one({'id': user_id})
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
        if 'last_login' in doc and isinstance(doc['last_login'], str):
            from datetime import datetime
            doc['last_login'] = datetime.fromisoformat(doc['last_login'].replace('Z', '+00:00'))
        
        return User.from_dict(doc)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Récupérer un utilisateur par nom d'utilisateur"""
        doc = self.collection.find_one({'username': username})
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
        if 'last_login' in doc and isinstance(doc['last_login'], str):
            from datetime import datetime
            doc['last_login'] = datetime.fromisoformat(doc['last_login'].replace('Z', '+00:00'))
        
        return User.from_dict(doc)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Récupérer un utilisateur par email"""
        doc = self.collection.find_one({'email': email})
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
        if 'last_login' in doc and isinstance(doc['last_login'], str):
            from datetime import datetime
            doc['last_login'] = datetime.fromisoformat(doc['last_login'].replace('Z', '+00:00'))
        
        return User.from_dict(doc)
    
    def update_last_login(self, user_id: str):
        """Mettre à jour la dernière connexion"""
        from datetime import datetime
        self.collection.update_one(
            {'id': user_id},
            {'$set': {'last_login': datetime.utcnow().isoformat()}}
        )