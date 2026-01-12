from src.services.auth_service import AuthService
from src.schemas.auth import TokenPair
from src.core.exceptions import IncorrectCredentials

class RefreshTokenUseCase:
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        
    async def execute(self, refresh_token: str) -> TokenPair:
        user_uuid = self.auth_service.validate_refresh_token(refresh_token)
        
        if not user_uuid:
            raise IncorrectCredentials("Invalid or expired refresh token")
        
        new_access = self.auth_service.create_access_token(subject=user_uuid)
        new_refresh = self.auth_service.create_refresh_token(subject=user_uuid)
        
        return TokenPair(
            access_token=new_access,
            refresh_token=new_refresh
        )