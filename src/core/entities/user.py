# src/core/entities/user.py
from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, Field

class UserEntity(BaseModel):
    uuid: str
    username: str
    hashed_pw: str
    email: EmailStr
    created_at: datetime = Field(
        default_factory=lambda _: datetime.now(tz=timezone.utc)
    )