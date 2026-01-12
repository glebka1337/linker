from src.services.auth_service import AuthService
from src.usecases.user.refresh import RefreshTokenUseCase

async def get_refresh_usecase() -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        auth_service=AuthService()
    )