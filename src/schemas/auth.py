import re
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8, max_length=64)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, pw) -> str:
        if not re.search(r'[A-Z]', pw):
            raise ValueError("Password must contain upper case latters")
        
        if not re.search(r'[a-z]', pw):
            raise ValueError("Password must contain lower case latters")
        
        if not re.search(r'[0-9]', pw):
            raise ValueError("Password must contain digits")
        
        return pw
    
class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    user_uuid: str