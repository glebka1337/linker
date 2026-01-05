from src.core.exceptions import NoteFoundError
from src.core.resources import Resources
from src.repos.mongo_repo import MongoRepo
from src.repos.vector_repo import QudrantVectorRepo
from src.services.queue_service_02 import RabbitQueueService
from src.workers.base import BaseWorker
from src.schemas.note import LinkTask, VectorizeTask
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
        self.ml_vectorize_service = MLService(
            model_name=settings.ML_MODEL_NAME,
            model_path=settings.ML_MODEL_PATH
        )
        
    async def setup(self, res: Resources) -> None:
        # we need to get access to notes, so we will define note repo
        await self.ml_vectorize_service.init_model()
        self.note_repo = MongoRepo(
            NoteDoc
        )
        
        # vector repo
        self.vector_repo = QudrantVectorRepo(
            client=res.qdrant_client,
            logger=self.logger
        )
        
        # queue to send a link task
        self.queue_service = RabbitQueueService(conn=res.rabbitmq_conn)
        self.logger.info("All repositories and services for vectorizer has been created.")
        
    async def run(self):
        return await super().run()
    
    async def process_task(
        self,
        task: VectorizeTask,
    ):
        # get a note text
        
        note = await self.note_repo.get_by_uuid(
            task.note_uuid
        )
        
        if not note:
            raise NoteFoundError(f"Note not found: uuid={task.note_uuid}")
        
        self.logger.info(f"Turn note {task.note_uuid} to vector...")
        
        vec = await self.ml_vectorize_service.vectorize(
            text=note.text
        )
        
        # upsert created vector
        
        await self.vector_repo.upsert(
            note_uuid=task.note_uuid,
            vector=vec
        )
        
        # create a task
        await self.queue_service.send_msg(
            msg=LinkTask(
                note_uuid=task.note_uuid,
                vector=vec
            ),
            queue_name=settings.LINK_TASK_QUEUE_NAME
        )
        
        self.logger.info(f"Link task has been created and sent to the queue.")
        return
        
        
    