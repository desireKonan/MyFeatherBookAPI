from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass


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
    created_at: str
    updated_at: str


