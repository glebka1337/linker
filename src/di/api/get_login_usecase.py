# src/di/api/get_login_usecase.py
from src.repos.user_mongo_repo import UserMongoRepo
from src.services.auth_service import AuthService
from src.usecases.user.login import LoginUserUseCase

async def get_login_usecase() -> LoginUserUseCase:
    
    repo = UserMongoRepo()
    return LoginUserUseCase(
        user_repo=repo,
        auth_service=AuthService()
    )