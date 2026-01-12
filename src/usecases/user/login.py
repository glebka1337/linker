from src.core.exceptions import IncorrectCredentials
from src.interfaces.user_repo_interface import UserRepo
from src.schemas.auth import TokenPair, UserLogin
from src.services.auth_service import AuthService


class LoginUserUseCase:
    
    def __init__(
        self,
        auth_service: AuthService,
        user_repo: UserRepo
    ):
        self.auth_service = auth_service
        self.user_repo = user_repo
    
    async def execute(
        self,
        user_data: UserLogin
    ) -> TokenPair: # type: ignore
        
        
        user = await self.user_repo.get_by_email(user_data.email)
        exception = IncorrectCredentials("Wrong email or password")
        
        if not user:
            raise exception
        
        if not self.auth_service.verify_password(
            plain_password=user_data.password,
            hashed_password=user.hashed_pw
        ):
            raise exception
        
        return TokenPair(
            access_token=self.auth_service.create_access_token(
                subject=user.uuid
            ),
            refresh_token=self.auth_service.create_refresh_token(
                subject=user.uuid
            )
        )