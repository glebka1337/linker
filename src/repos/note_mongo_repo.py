from typing import List, Optional
from src.repos.base_mongo_repo import BaseMongoRepo
from src.models.note import Note as NoteDoc
from src.core.entities.note import NoteEntity
from src.schemas.note import NoteTitleProjection
import logging

logger = logging.getLogger(__name__)

class NoteMongoRepo(BaseMongoRepo[NoteDoc, NoteEntity]):
    
    def __init__(self):
        super().__init__(model=NoteDoc)

    async def get_by_uuid(
        self,
        note_uuid: str,
        owner_uuid: str
    ) -> Optional[NoteEntity]:
        q = {
            "uuid": note_uuid,
            "owner_uuid": owner_uuid
        }
        doc = await self._find_one(q)
        
        if not doc: return None
        return self._to_entity(doc)

    async def get_by_uuids(
        self,
        uuids: List[str],
        owner_uuid: str,
        lim: Optional[int] = None
    ) -> List[NoteEntity]:
        q = {
            "uuid": {"$in": uuids},
            "owner_uuid": owner_uuid
        }
        docs = await self._find_many(q, limit=lim)
        return [self._to_entity(d) for d in docs]
        
    async def get_titles_by_uuids(
        self,
        uuids: List[str],
        owner_uuid: str
    ) -> List[NoteTitleProjection]:
        filter_q = {
            "uuid": {"$in": uuids},
            "owner_uuid": owner_uuid
        }
        
        results = await self.model.find(filter_q)\
            .project(NoteTitleProjection)\
            .to_list()
            
        return results

    async def get_all(
        self,
        owner_uuid: str
    ) -> List[NoteEntity]:
        docs = await self._find_many({"owner_uuid": owner_uuid})
        return [self._to_entity(d) for d in docs]

    async def create(
        self,
        note_data: NoteEntity
    ) -> NoteEntity:
        doc = self._to_doc(note_data)
        created_doc = await self._insert(doc)
        return self._to_entity(created_doc)

    async def update(
        self,
        note: NoteEntity,
        owner_uuid: str
    ) -> Optional[NoteEntity]:
        filter_query = {
            "uuid": note.uuid,
            "owner_uuid": owner_uuid
        }
        doc = await self._find_one(filter_query)
        
        if not doc: return None
        
        await doc.set(note.model_dump(exclude={'id', '_id'}))

        return self._to_entity(doc)

    async def delete(
        self,
        note_uuid: str,
        owner_uuid: str
    ) -> bool:
        doc = await self._find_one({
            "uuid": note_uuid,
            "owner_uuid": owner_uuid
        })
        
        if not doc:
            return False

        await self._delete(doc)
        return True

    async def remove_related_links(
        self,
        target_uuid: str,
        owner_uuid: str
    ):
        await self._update_many_raw(
            filter_q={"owner_uuid": owner_uuid},
            update_q={"$pull": {"related_notes": {"note_uuid": target_uuid}}}
        )

    # --- Mappers ---
    def _to_entity(self, doc: NoteDoc) -> NoteEntity: 
        return NoteEntity(**doc.model_dump())

    def _to_doc(self, entity: NoteEntity) -> NoteDoc: 
        return self.model(**entity.model_dump())