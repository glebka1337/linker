from typing import Protocol

from src.core.entities.user import UserEntity


class UserRepo(Protocol):
    """
    Interface representing an repo for managing users
    """
    
    async def create(
        self,
        user_data: UserEntity 
    ) -> UserEntity:
        """
        Creates a new user
        """
        ...
    
    async def get_by_email(
        self,
        email: str
    ) -> UserEntity | None:
        """
        Returns a user by email given. 
        If exists returns user entity, if not -> None
        """
        ...