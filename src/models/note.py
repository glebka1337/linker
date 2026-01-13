from datetime import datetime, timezone
from typing import Annotated, List
from beanie import Document, Indexed
from pydantic import Field
from uuid import uuid4

from src.schemas.note import RelatedNote

class Note(Document):
    uuid: str = Field(
        default_factory=lambda: str(uuid4())
    )
    owner_uuid: str
    title: Annotated[str, Indexed(unique=True)]
    text: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    related_notes: List[RelatedNote] = Field(default_factory=list)
    
    