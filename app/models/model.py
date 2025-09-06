from enum import Enum
from .base_model import BaseModel
from datetime import datetime

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
        self.note_id = kwargs.get('note_id')
        
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
        attachment.note_id = self.id
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