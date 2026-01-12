from fastapi import APIRouter, Body, Depends, HTTPException, status
from src.di.api.get_login_usecase import get_login_usecase
from src.schemas.auth import UserLogin, UserRegister, TokenPair
from src.di.api.get_register_usecase import get_register_usecase
from src.usecases.user.login import LoginUserUseCase
from src.usecases.user.refresh import RefreshTokenUseCase
from src.usecases.user.register import RegisterUserUseCase
from src.di.api.get_refresh_usecase import get_refresh_usecase
from src.core.exceptions import IncorrectCredentials, UserAlreadyExistsError
import logging

logger = logging.getLogger(__name__)

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/register", response_model=TokenPair)
async def register_user(
    user_data: UserRegister,
    usecase: RegisterUserUseCase = Depends(get_register_usecase)
):
    try:
        return await usecase.execute(user_data)
        
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@auth_router.post("/login", response_model=TokenPair)
async def login_user(
    user_login: UserLogin,
    usecase: LoginUserUseCase = Depends(get_login_usecase)
):
    try:
      return await usecase.execute(user_login)
    except IncorrectCredentials:
        raise HTTPException(
            detail="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
      logger.critical(f'Unexpected error occured: {e}' ,exc_info=True)
      raise HTTPException(
          detail="Login failed.",
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

@auth_router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    # Body(..., embed=True) означает, что мы ждем JSON {"refresh_token": "строка"}
    refresh_token: str = Body(..., embed=True),
    usecase: RefreshTokenUseCase = Depends(get_refresh_usecase)
):
    try:
        return await usecase.execute(refresh_token)
        
    except IncorrectCredentials:
        # Если рефреш не валиден — 401. Фронт перекинет на страницу логина.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Refresh error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refresh failed"
        )