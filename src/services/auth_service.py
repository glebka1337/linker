from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.core.config import settings
from src.core.exceptions import IncorrectCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None) -> str:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expire, "sub": str(subject)}
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def validate_refresh_token(
        token: str
    ) -> str | None:
        """
        Decodes refresh token and returns user_uuid if valid
        """
        
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            user_uuid = payload.get('sub', None) # type: ignore
            
            return user_uuid
    
        except JWTError:
            return None
      
    @staticmethod
    def create_refresh_token(subject: Union[str, Any]) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) 
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt