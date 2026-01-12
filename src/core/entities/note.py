# src/core/entities.py
import pydantic
from datetime import datetime, timezone
from typing import List
import uuid

class NoteEntity(pydantic.BaseModel):
    uuid: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    owner_uuid: str
    title: str
    text: str
    created_at: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    related_notes: List['RelatedNoteEntity'] = pydantic.Field(default_factory=list)

class RelatedNoteEntity(pydantic.BaseModel):
    note_uuid: str
    score: float