from src.schemas.auth import UserRegister, TokenPair
from src.interfaces.user_repo_interface import UserRepo
from src.services.auth_service import AuthService
from src.core.entities.user import UserEntity
from src.core.exceptions import UserAlreadyExistsError 
import uuid

class RegisterUserUseCase:
    
    def __init__(self, repo: UserRepo, auth_service: AuthService):
        self.repo = repo
        self.auth_service = auth_service
        
    async def execute(self, data: UserRegister) -> TokenPair:
        # 1. Check Email uniqueness
        existing_email = await self.repo.get_by_email(data.email)
        if existing_email:
            raise UserAlreadyExistsError(f"User with email {data.email} already exists")
            
        # 2. Check Username uniqueness (New Logic)
        existing_username = await self.repo.get_by_username(data.username)
        if existing_username:
            raise UserAlreadyExistsError(f"User with username {data.username} already exists")
            
        # 3. Hash password
        hashed_pw = self.auth_service.get_password_hash(data.password)
        
        # 4. Create Entity
        new_user = UserEntity(
            uuid=str(uuid.uuid4()),
            email=data.email,
            username=data.username,
            hashed_pw=hashed_pw
        )
        
        # 5. Save to DB
        await self.repo.create(new_user)
        
        # 6. Generate Tokens
        access = self.auth_service.create_access_token(new_user.uuid)
        refresh = self.auth_service.create_refresh_token(new_user.uuid)
        
        return TokenPair(
            access_token=access,
            refresh_token=refresh
        )