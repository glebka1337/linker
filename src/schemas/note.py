from datetime import datetime, timezone
from typing import List
from pydantic import (
    BaseModel,
    Field
)

class NoteBase(BaseModel):
    title: str
    text: str = Field(..., max_length=1000)

class RelatedNote(BaseModel):
    """
    Represents related note in a simple way.
    Contains only necessary info: uuid and score (cosine sim)

    Args:
        BaseModel (_type_): _description_
    """
    note_uuid: str
    score: float

class NoteCreate(NoteBase):
    ...
    
class NoteRead(NoteBase):
    uuid: str
    title: str
    text: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    related_notes: List[RelatedNote] = Field(default_factory=list)
    
class NoteUpdate(BaseModel):
    title: str | None
    text: str | None

class VectorizeTask(BaseModel):
    force_update: bool = False
    note_uuid: str

class LinkTask(BaseModel):
    vector_link_treshold: float = 0.75
    note_uuid: str
    vector: list[float]
    