from src.repos.user_mongo_repo import UserMongoRepo
from src.services.auth_service import AuthService
from src.usecases.user.register import RegisterUserUseCase

async def get_register_usecase() -> RegisterUserUseCase:
    return RegisterUserUseCase(
        repo=UserMongoRepo(),       
        auth_service=AuthService() 
    )