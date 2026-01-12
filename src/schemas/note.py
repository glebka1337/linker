from datetime import datetime, timezone
from typing import List
from pydantic import (
    BaseModel,
    Field
)

class NoteBase(BaseModel):
    """
    Base model for representing note model

    Args:
        BaseModel (_type_):
    """
    title: str
    text: str = Field(..., max_length=1000)

class NoteShortRead(NoteBase):
    uuid: str
    title: str
    text: str
    created_at: datetime
    related_notes: List["RelatedNote"] = Field(default_factory=list)

class RelatedNote(BaseModel):
    """
    Represents related note in a simple way.
    Contains only necessary info: uuid and score (cosine sim)
    Stored in database
    Args:
        BaseModel (_type_): _description_
    """
    note_uuid: str
    score: float
    
class RelatedNoteResponse(BaseModel):
    """
    Responsible for represantation of a realted notes with titles included
    """
    uuid: str
    title: str | None = None
    score: float

class NoteTitleProjection(BaseModel):
    """
    Created for reducing data retrieval, only title and uuid
    """
    uuid: str
    title: str

class NoteCreate(NoteBase):
    pass
    
class NoteRead(NoteBase):
    uuid: str
    title: str
    text: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    related_notes: List[RelatedNoteResponse] = Field(default_factory=list)
    
class NoteUpdate(BaseModel):
    title: str | None
    text: str | None

class VectorizeTask(BaseModel):
    note_uuid: str
    owner_uuid: str  
    force_update: bool = False

class LinkTask(BaseModel):
    note_uuid: str
    owner_uuid: str  
    vector: list[float]
    vector_link_treshold: float = 0.75
    