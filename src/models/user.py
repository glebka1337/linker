# src/models/user.py
from datetime import datetime, timezone
from beanie import Document, Indexed
from typing import Annotated

class User(Document):
    uuid: Annotated[str, Indexed(unique=True)]
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[str, Indexed(unique=True)]
    username: str
    hashed_pw: str
    created_at: datetime = datetime.now(tz=timezone.utc)
    
    class Settings:
        name = 'users'