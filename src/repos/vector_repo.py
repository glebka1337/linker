# src/repos/vector_repo.py
from src.core.config import settings
from typing import List, cast
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import (
    UnexpectedResponse
)
from qdrant_client.http.models import (
    Filter, HasIdCondition, PointStruct
)
from qdrant_client.models import VectorParams, Distance
from src.interfaces.vector_repo_interface import VectorSearchResult
from src.utils.safe_exec import ErrMappingType, safe_exec
import logging

logger = logging.getLogger(__name__)

class QdrantVectorRepo:    
    
    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str = settings.QDRANT_COLLECTION_NAME,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.error_mapping: ErrMappingType = {
            ConnectionError: "Can not connect to a client",
            UnexpectedResponse: "Qdrant API error",
            Exception: "Unknown error"
        }
        self.logger = logger
    
    async def search(
        self,
        vector: List[float],
        limit: int = 10,
        treshold: float = 0.75,
        excluded_note_uuid: str | None = None
    ) -> List[VectorSearchResult]: 
        async with safe_exec(
            err_mapping=self.error_mapping,
            logger=self.logger,
            throw=True
        ):
            
            query_filter = None
            if excluded_note_uuid:
                query_filter = Filter(
                    must_not=[
                        HasIdCondition(
                            has_id=[excluded_note_uuid] # pyright: ignore[reportArgumentType]
                        )
                    ],
                )
            
            result = await self.client.query_points(
                query=vector,
                collection_name=self.collection_name,
                query_filter=query_filter,
                limit=limit,
                score_threshold=treshold
            )
            
            self.logger.info(f"Found {len(result.points)} vectors for {vector[:5]}...")
            
            return [
                VectorSearchResult(
                    note_uuid=str(p.id),
                    score=p.score
                )
                for p in result.points
            ]
    
    async def get_vec_by_uuid(
        self,
        note_uuid: str
    ) -> List[float] | None:
        async with safe_exec(
            err_mapping=self.error_mapping,
            logger=self.logger,
            throw=True
        ):
            points = await self.client.retrieve(
                collection_name=self.collection_name,
                ids=[note_uuid],
                with_vectors=True
            )
            
            if not points:
                self.logger.info(f"No vectors found for note_uuid: {note_uuid}")
                return None
            
            return cast(List[float], points[0].vector)
    
    async def upsert(
        self,
        note_uuid: str,
        vector: List[float],
    ) -> None:
        async with safe_exec(
            err_mapping=self.error_mapping,
            logger=self.logger,
            throw=True
        ):
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=note_uuid,
                        vector=vector,
                    )
                ],
                wait=True
            )
            
            self.logger.info(f"Updated/inserted vector {vector[:3]}...")
        
    async def delete(
        self,
        note_uuid: str
    ) -> None:
        async with safe_exec(
            err_mapping=self.error_mapping,
            logger=self.logger,
            throw=True
        ):
            
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=[note_uuid]
            )
            
            self.logger.info(f"Deleted vector for note: uuid={note_uuid}")
            
    async def ensure_collection(
        self,
        vector_size: int
    ) -> None:
        
        if await self.client.collection_exists(
            collection_name=self.collection_name
        ):
            self.logger.info(f"Collection {self.collection_name} already exists, skip creating.")
            return
        
        self.logger.info(f"Collection {self.collection_name} does not exists, creating...")
        
        try:
            
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    distance=Distance.COSINE,
                    size=vector_size
                )
            )
            
        except Exception as e:
            self.logger.critical(f"Error during creating collection: {e}")
            raise e