from typing import Protocol, List, Annotated
from pydantic import BaseModel

class VectorSearchResult(BaseModel):
    note_uuid: str
    score: float 

class NoteVectorRepo(Protocol):
    """
    Manages note vectors.
    Every note has vector. 
    Mapping is flowing: note_uuid <-> vec_uuid
    """
    async def search(
        self,
        vector: List[float],
        limit: int = 10,
        treshold: Annotated[float, "Cosine similarity score"] = 0.75,
        excluded_note_uuid: Annotated[str | None, "UUID of a note vector to exclude (to avoid self relation)"] = None
    ) -> List[VectorSearchResult]:
        ...
    
    async def get_vec_by_uuid(
        self,
        note_uuid: str
    ) -> List[float] | None: ...
    
    async def upsert(
        self,
        note_uuid: str,
        vector: List[float],
    ) -> None: ...
    
    async def delete(
        self,
        note_uuid: str
    ) -> None: ...