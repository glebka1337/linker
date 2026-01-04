from contextlib import asynccontextmanager
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance
from src.core.config import settings

def create_qdrant_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(
        url=settings.QDRANT_DB_URL
    )

@asynccontextmanager
async def qdrant_client_manager():
    client = create_qdrant_client()
    try:
        yield client
    finally:
        await client.close()

async def create_qdrant_collection(
    client: AsyncQdrantClient,
    vector_size: int,
    collection_name: str = settings.QDRANT_COLLECTION_NAME  
) -> None:
    
    if await client.collection_exists(
        collection_name=collection_name
    ): return
    
    await client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            distance=Distance.COSINE,
            size=vector_size
        )
    ) 