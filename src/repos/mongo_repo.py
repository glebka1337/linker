from typing import List, Optional, TypeVar, Type, Generic
from src.core.entities.note import NoteEntity
from pymongo.errors import PyMongoError
from src.schemas.note import NoteTitleProjection
from src.utils.safe_exec import safe_exec
from beanie import Document
import logging

logger = logging.getLogger(__name__)

DocType = TypeVar("DocType", bound=Document)

class MongoRepo(Generic[DocType]):
    
    def __init__(self, model: Type[DocType]) -> None:
        self.model = model
        self.err_mapping = {
            PyMongoError: "MongoDB internal error",
            Exception: "Unknown error occurred"
        }
    
    async def get_by_uuid(
        self,
        note_uuid: str,
        owner_uuid: str
    ) -> Optional[NoteEntity]:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True):
            note = await self.model.find_one({
                "uuid": note_uuid,
                "owner_uuid": owner_uuid
            })
            
            if not note: return None
            return self._to_entity(note)
    
    async def get_by_uuids(
        self,
        uuids: List[str],
        owner_uuid: str,
        lim: Optional[int] = None
    ) -> List[NoteEntity]:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True): 
            filter_query = {
                "uuid": {"$in": uuids},
                "owner_uuid": owner_uuid
            }
            
            query = self.model.find(filter_query)
            if lim:
                query.limit(lim)
                
            docs = await query.to_list()
            return [self._to_entity(doc) for doc in docs]
    
    async def get_all(
        self,
        owner_uuid: str
    ) -> List[NoteEntity]:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True):
            docs = await self.model.find({"owner_uuid": owner_uuid}).to_list()
            return [self._to_entity(doc) for doc in docs]
            
    async def get_titles_by_uuids(
        self,
        uuids: List[str],
        owner_uuid: str
    ) -> List[NoteTitleProjection]:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True):
            filter_q = {
                "uuid": {"$in": uuids},
                "owner_uuid": owner_uuid
            }
            
            results = await self.model.find(filter_q) \
                        .project(NoteTitleProjection).to_list()
            return results
            
    async def delete(
        self,
        note_uuid: str,
        owner_uuid: str
    ) -> bool:
        async with safe_exec(logger=logger, err_mapping=self.err_mapping, throw=True):
            note = await self.model.find_one({
                "uuid": note_uuid,
                "owner_uuid": owner_uuid
            })
            
            if not note:
                return False

            await note.delete()
            return True

    async def remove_related_links(
        self,
        target_uuid: str,
        owner_uuid: str
    ):
        async with safe_exec(logger=logger, err_mapping=self.err_mapping, throw=True):
            await self.model.get_pymongo_collection().update_many(
                {"owner_uuid": owner_uuid},
                {"$pull": {"related_notes": {"note_uuid": target_uuid}}}
            )
     
    async def create(
        self,
        note_data: NoteEntity
    ) -> NoteEntity:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True):
            new_doc = self._to_doc(note_data)
            await new_doc.insert()
            return self._to_entity(new_doc)
    
    async def update(
        self,
        note: NoteEntity,
        owner_uuid: str
    ) -> Optional[NoteEntity]:
        async with safe_exec(err_mapping=self.err_mapping, logger=logger, throw=True):
            filter_query = {
                "uuid": note.uuid,
                "owner_uuid": owner_uuid
            }
            doc = await self.model.find_one(filter_query)
            
            if not doc: return None
            

            await doc.set(note.model_dump(
                exclude={'id', '_id'}
            ))
            
            return self._to_entity(doc)
            
    def _to_entity(self, doc: DocType) -> NoteEntity: 
        return NoteEntity(**doc.model_dump())

    def _to_doc(self, entity: NoteEntity) -> DocType: 
        return self.model(**entity.model_dump())