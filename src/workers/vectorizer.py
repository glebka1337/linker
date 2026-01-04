from src.core.resources import Resources
from src.interfaces.model_service_interface import ModelServiceInterface
from src.interfaces.note_repo_interface import NoteRepo
from src.repos.mongo_repo import MongoRepo
from src.repos.vector_repo import QudrantVectorRepo
from src.workers.base import BaseWorker
from src.schemas.note import VectorizeTask
from src.core.config import settings
from src.services.ml_service import MLService
from src.models.note import Note as NoteDoc
import logging

logger = logging.getLogger(__name__)

class VectorWorker(BaseWorker[VectorizeTask]):
    
    task_schema = VectorizeTask
    queue_name = settings.VECTORIZE_TASK_QUEUE_NAME

    def __init__(
        self
    ) -> None:
        super().__init__()
        self.model_service = MLService(
            model_name=settings.ML_MODEL_NAME,
            model_path=settings.ML_MODEL_PATH
        )
        self.note_repo = MongoRepo(model=NoteDoc)
        
    async def run(self):
        await self.model_service.init_model()
        return await super().run()
    
    async def process_task(
        self,
        task: VectorizeTask,
        resources: Resources
    ):
        # we need to get note from mongo
        note = await self.note_repo.get_by_uuid(
            note_uuid=task.note_uuid
        )
        
        if not note:
            return
        
        vec = await self.model_service.vectorize(
            text=note.text
        )
        
        vec_repo = QudrantVectorRepo(
            client=resources.qdrant_client,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            logger=logger
        )
        
        await vec_repo.upsert(
            note_uuid=note.uuid,
            vector=vec
        )
        
        
        
        
    