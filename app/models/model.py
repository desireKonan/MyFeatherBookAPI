from enum import Enum
from .base_model import BaseModel
from app.utils.jwt_manager import jwt_manager

class AttachmentType(Enum):
    """Types de documents utilises pour notre projet"""
    AUDIO = "Audio"
    DOCUMENT = "Document"


class Attachment(BaseModel):
    """Model for attachments (no persistence)."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = kwargs.get('url', '')
        self.type = kwargs.get('type')
        
        # Convert string to enum if needed
        if isinstance(self.type, str):
            self.type = AttachmentType(self.type)
    
    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.type.value if self.type else None
        return data


class Note(BaseModel):
    """Model for notes (no persistence)."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = kwargs.get('content', '')
        self.attachments = kwargs.get('attachments', [])
        
        # Convert attachment dictionaries to Attachment objects
        if self.attachments and isinstance(self.attachments[0], dict):
            self.attachments = [Attachment(**att) for att in self.attachments]
    
    def add_attachment(self, attachment):
        if not isinstance(attachment, Attachment):
            attachment = Attachment(**attachment)
        self.attachments.append(attachment)
    
    def to_dict(self):
        data = super().to_dict()
        data['attachments'] = [attachment.to_dict() for attachment in self.attachments]
        return data


class Synthesis(BaseModel):
    """Model for synthesis (no persistence)."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = kwargs.get('url', '')
        self.is_generated = kwargs.get('is_generated', False)
    
    def to_dict(self):
        return super().to_dict()



class User(BaseModel):
    """Modèle utilisateur"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get('username', '')
        self.email = kwargs.get('email', '')
        self.password_hash = kwargs.get('password_hash', '')
        self.role = kwargs.get('role', 'user')  # user, admin
        self.is_active = kwargs.get('is_active', True)
        self.last_login = kwargs.get('last_login')
    
    def set_password(self, password):
        """Définir le mot de passe"""
        self.password_hash = jwt_manager.hash_password(password)
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return jwt_manager.check_password(password, self.password_hash)
    
    def to_dict(self):
        data = super().to_dict()
        # Ne pas exposer le hash du mot de passe
        data.pop('password_hash', None)
        return data
    
    def to_dict_with_token(self):
        """Retourner les données utilisateur avec token"""
        data = self.to_dict()
        data['token'] = jwt_manager.generate_token(self.id, self.username, self.role)
        return data