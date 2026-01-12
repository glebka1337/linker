from typing import Optional
from src.repos.base_mongo_repo import BaseMongoRepo
from src.models.user import User as UserDoc
from src.core.entities.user import UserEntity

class UserMongoRepo(BaseMongoRepo[UserDoc, UserEntity]):
    
    def __init__(self):
        super().__init__(model=UserDoc)

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        doc = await self._find_one({"email": email})
        
        if not doc:
            return None
            
        return self._to_entity(doc)

    async def create(self, user_data: UserEntity) -> UserEntity:
        doc = self._to_doc(user_data)
        
        created_doc = await self._insert(doc)
        
        return self._to_entity(created_doc)

    # --- Mappers ---
    def _to_entity(self, doc: UserDoc) -> UserEntity:
        return UserEntity(**doc.model_dump())

    def _to_doc(self, entity: UserEntity) -> UserDoc:
        return UserDoc(**entity.model_dump())