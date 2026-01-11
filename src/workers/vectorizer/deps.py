# src/workers/vectorizer/deps.py
from dataclasses import dataclass
import logging
from httpx import AsyncClient
from src.core.resources import Resources
from src.interfaces.vector_repo_interface import NoteVectorRepo
from src.interfaces.note_repo_interface import NoteRepo
from src.interfaces.queue_interface import QueueServiceInterface
from src.models.note import Note as NoteDoc
from src.core.config import settings
from src.repos.mongo_repo import MongoRepo
from src.repos.vector_repo import QdrantVectorRepo
from src.services.queue_service import RabbitQueueService 
from src.services.ml_gateway_service import MLGatewayService

logger = logging.getLogger(__name__)

@dataclass
class VectorWorkerDeps:
    note_repo: NoteRepo
    vector_repo: NoteVectorRepo
    queue_service: QueueServiceInterface
    ml_gateway: MLGatewayService

async def assemble_vectorizer(
    resources: Resources
) -> VectorWorkerDeps: 
    logger.info("Assembling all dependencies for vectorize worker")
    
    if not resources.qdrant_client:
        raise RuntimeError("Error: can not assemble vectorizer deps without qdrant client")
    
    if not resources.rabbitmq_conn:
        raise RuntimeError("Error: can not assemble vectorizer deps without rabbitmq conn")

    note_repo = MongoRepo(NoteDoc)
    queue_service = RabbitQueueService(conn=resources.rabbitmq_conn)
    
    httpx_client = AsyncClient(
        base_url=settings.ML_SERVICE_URL,
        timeout=30.0
    )
    
    ml_gateway = MLGatewayService(client=httpx_client)
    
    try:
        dim = await ml_gateway.get_dimension()
        logger.info(f'Dimension is: {dim}')
    except Exception as e:
        logger.critical(f'Cannot get dimension of vectors: {e}')
        await httpx_client.aclose()
        raise e
    
    vector_repo = QdrantVectorRepo(
        client=resources.qdrant_client,
        collection_name=settings.QDRANT_COLLECTION_NAME
    )
    
    try:
        await vector_repo.ensure_collection(vector_size=dim)
    except Exception as e:
        logger.critical(f'Error during creating collection: {e}')
        await httpx_client.aclose()
        raise e
    
    return VectorWorkerDeps(
        note_repo=note_repo,
        vector_repo=vector_repo,
        queue_service=queue_service,
        ml_gateway=ml_gateway
    )