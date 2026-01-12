from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic, Optional, List, Any, Dict
from beanie import Document
from pydantic import BaseModel
from pymongo.errors import PyMongoError
from src.utils.safe_exec import safe_exec
import logging

# T - Database Document (Beanie)
DocType = TypeVar("DocType", bound=Document)
# E - Domain Entity (Pydantic)
EntityType = TypeVar("EntityType", bound=BaseModel)

class BaseMongoRepo(ABC, Generic[DocType, EntityType]):
    """
    Abstract Base Class for MongoDB Repositories.
    1. ABC - Prevents direct instantiation of this class.
    2. Enforces implementation - Requires subclasses to implement data mappers.
    """
    
    def __init__(self, model: Type[DocType]):
        self.model = model
        # Logger dynamically uses the name of the concrete subclass (e.g., UserRepo, NoteRepo)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.err_mapping = {
            PyMongoError: "MongoDB internal error",
            Exception: "Unknown error occurred"
        }

    # --- Abstract Methods (Contract) ---
    # The subclass MUST implement these, otherwise Python will raise a TypeError at runtime.

    @abstractmethod
    def _to_entity(self, doc: DocType) -> EntityType:
        """Converts database document to domain entity"""
        pass

    @abstractmethod
    def _to_doc(self, entity: EntityType) -> DocType:
        """Converts domain entity to database document"""
        pass

    # --- Base Logic (Shared Infrastructure) ---
    
    async def _insert(self, doc: DocType) -> DocType:
        async with safe_exec(err_mapping=self.err_mapping, logger=self.logger, throw=True):
            await doc.insert()
            return doc
            
    async def _find_one(self, query: Dict[str, Any]) -> Optional[DocType]:
        async with safe_exec(err_mapping=self.err_mapping, logger=self.logger, throw=True):
            return await self.model.find_one(query)

    async def _find_many(self, query: Dict[str, Any], limit: int | None = None) -> List[DocType]:
        async with safe_exec(err_mapping=self.err_mapping, logger=self.logger, throw=True):
            q = self.model.find(query)
            if limit:
                q.limit(limit)
            return await q.to_list()
            
    async def _delete(self, doc: DocType) -> None:
        async with safe_exec(err_mapping=self.err_mapping, logger=self.logger, throw=True):
            await doc.delete()
            
    async def _update_many_raw(self, filter_q: dict, update_q: dict):
        """
        Executes a raw update_many command via the Motor driver.
        Useful for complex operators like $pull where Beanie might be limited.
        """
        async with safe_exec(err_mapping=self.err_mapping, logger=self.logger, throw=True):
            await self.model.get_pymongo_collection().update_many(filter_q, update_q)