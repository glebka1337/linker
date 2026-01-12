from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from src.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user_uuid(
    creds: HTTPAuthorizationCredentials = Depends(security)
):
    exception = HTTPException(
        detail="Could not validate credentials",
        status_code=401,
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    
    token = creds.credentials
    
    try:
      payload = jwt.decode(
          token=token,
          key=settings.SECRET_KEY,
          algorithms=[settings.ALGORITHM],
      )
      user_uuid: str = payload.get('sub', None) # type: ignore
      
      if not user_uuid:
          raise exception
      
      return user_uuid
  
    except JWTError:
      raise exception
    