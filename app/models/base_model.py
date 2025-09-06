from datetime import datetime
import uuid

class BaseModel:
    """Base domain model (no persistence)."""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        
        # Set other declared attributes on subclass
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Serialize model to dict (for transport/persistence)."""
        data = {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        for attr in dir(self):
            if attr in ('id', 'created_at', 'updated_at'):
                continue
            if attr.startswith('_'):
                continue
            value = getattr(self, attr, None)
            if callable(value):
                continue
            if value is not None:
                data[attr] = value
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)