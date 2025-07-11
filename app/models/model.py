from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class AttachmentType(Enum):
    """ Ici les types de documents utilises pour notre projet """
    AUDIO = "Audio"
    DOCUMENT = "Document"


@dataclass
class Attachment(BaseModel):
    url: str
    type: AttachmentType


@dataclass
class Note(BaseModel):
    content: str
    attachments: list[Attachment]
    created_at: datetime
    updated_at: datetime


@dataclass
class Synthesis(BaseModel):
    id: int
    url: str
    is_generated: bool
    created_at: datetime
    updated_at: datetime


