from typing import Optional
from src.repos.base_mongo_repo import BaseMongoRepo
from src.models.user import User as UserDoc
from src.core.entities.user import UserEntity

class UserMongoRepo(BaseMongoRepo[UserDoc, UserEntity]):
    
    def __init__(self):
        super().__init__(model=UserDoc)

    # --- Public Interface Methods ---

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        return await self._find_by_field("email", email)

    async def get_by_username(self, username: str) -> Optional[UserEntity]:
        return await self._find_by_field("username", username)

    async def create(self, user_data: UserEntity) -> UserEntity:
        doc = self._to_doc(user_data)
        
        created_doc = await self._insert(doc)
        
        return self._to_entity(created_doc)

    # --- Private Helper (The Magic) ---
    
    async def _find_by_field(self, field: str, value: str) -> Optional[UserEntity]:
        """
        Universal helper to find a doc by any single field and map it.
        Reduces duplication for get_by_email, get_by_username, etc.
        """
        doc = await self._find_one({field: value})
        if not doc:
            return None
        return self._to_entity(doc)

    # --- Mappers ---
    def _to_entity(self, doc: UserDoc) -> UserEntity:
        return UserEntity(**doc.model_dump())

    def _to_doc(self, entity: UserEntity) -> UserDoc:
        return UserDoc(**entity.model_dump())