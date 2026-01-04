# src/core/entities.py
import pydantic
from datetime import datetime, timezone
from typing import List
import uuid

class NoteEntity(pydantic.BaseModel):
    uuid: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    text: str
    created_at: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    related_notes: List['RelatedNotEntity'] = pydantic.Field(default_factory=list)

class RelatedNotEntity(pydantic.BaseModel):
    note_uuid: str
    score: float