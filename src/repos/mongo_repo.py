from typing import List
from src.core.entities.note import NoteEntity
from pymongo.errors import PyMongoError
from src.utils.safe_exec import safe_exec
from typing import TypeVar, Type, Generic
from beanie import Document
import logging

logger = logging.getLogger(__name__)

DocType = TypeVar("DocType", bound=Document)

class MongoRepo(Generic[DocType]):
    
    
    def __init__(
        self,
        model: Type[DocType]
    ) -> None:
        self.model = model
        self.err_mapping = {
            PyMongoError: "MongoDB internal error",
            Exception: "Unknown error occured"
        }
    
    async def get_by_uuid(
        self,
        note_uuid: str
    ) -> NoteEntity | None:
        async with safe_exec(
            err_mapping=self.err_mapping,
            logger=logger,
            throw=True,
        ):
            note = await self.model.find_one({
                "uuid": note_uuid
            })
            
            if not note: return None
            
            return self._to_entity(
                note
            )
    
    async def get_by_uuids(
        self,
        uuids: List[str],
        lim: int | None = None
    ) -> List[NoteEntity]:
        async with safe_exec(
            err_mapping=self.err_mapping,
            logger=logger,
            throw=True
        ): 
            filter_query = {
                "uuid": {"$in": uuids}
            }
            
            query = self.model.find(
                filter_query
            )
            
            if lim:
                query.limit(lim)
                
            docs = await query.to_list()
                    
            return [
                self._to_entity(
                    doc
                )
                for doc in docs
            ]
    
    async def get_all(
        self,
    ) -> List[NoteEntity]:
        async with safe_exec(
            err_mapping=self.err_mapping,
            logger=logger,
            throw=True
        ):
            docs = await self.model.find_all().to_list()
            return [
                    self._to_entity(
                        doc
                    )
                    for doc in docs
                ]
    async def create(
        self,
        note_data: NoteEntity
    ) -> NoteEntity:
        async with safe_exec(
            err_mapping=self.err_mapping,
            logger=logger,
            throw=True
        ):
            new_doc = self._to_doc(
                note_data
            )
            
            await new_doc.insert()
            return self._to_entity(
                new_doc
            )
    
    async def update(
        self,
        note: NoteEntity
    ) -> NoteEntity | None:
        async with safe_exec(
            err_mapping=self.err_mapping,
            logger=logger,
            throw=True
        ):
            filter_query = {
                "uuid": note.uuid
            }
            doc = await self.model.find_one(filter_query)
            
            if not doc: return None
            await doc.set(note.model_dump(
                exclude={'id', '_id'}
            ))
            
            return self._to_entity(doc)
            
        
    # MAPPERS Domain <-> Models (ODM)
    def _to_entity(
        self, doc: DocType
    ) -> NoteEntity: 
        """Turns document to domain entity"""
        return NoteEntity(
            **doc.model_dump()
        )
    def _to_doc(
        self, entity: NoteEntity
    ) -> DocType: 
        """Turns entity to a mongo/beanie document"""
        return self.model(
            **entity.model_dump()
        )
    
    