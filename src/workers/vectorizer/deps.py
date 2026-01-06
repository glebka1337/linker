# src/workers/vectorizer/worker.py
from dataclasses import dataclass
from src.core.resources import Resources
from src.interfaces.model_service_interface import ModelServiceInterface
from src.interfaces.vector_repo_interface import NoteVectorRepo
from src.interfaces.note_repo_interface import NoteRepo
from src.interfaces.queue_interface import QueueService
from src.models.note import Note as NoteDoc
from src.core.config import settings
from src.repos.mongo_repo import MongoRepo
from src.repos.vector_repo import QdrantVectorRepo
from src.services.ml_service import MLService
from src.services.queue_service_02 import RabbitQueueService 
import logging

logger = logging.getLogger(__name__)

@dataclass
class VectorWorkerDeps:
  note_repo: NoteRepo
  vector_repo: NoteVectorRepo
  queue_service: QueueService
  ml_service: ModelServiceInterface



async def assemble_vectorizer(
    resources: Resources
) -> VectorWorkerDeps: 
    """
    Function to generate a dependecies for a VectorWorker

    Args:
        resources (Resources): _description_

    Returns:
        VectorizerDeps: _description_
    """
    logger.info(f"Assembling all dependencies for vectorize worker")
    
    note_repo = MongoRepo(
        NoteDoc
    )
    
    vector_repo = QdrantVectorRepo(
        client=resources.qdrant_client
    )
    
    queue_service = RabbitQueueService(conn=resources.rabbitmq_conn)
    
    ml_service = MLService(
        model_name=settings.ML_MODEL_NAME,
        model_path=settings.ML_MODEL_PATH
    )
    
    return VectorWorkerDeps(
        note_repo=note_repo,
        vector_repo=vector_repo,
        queue_service=queue_service,
        ml_service=ml_service
    )
    