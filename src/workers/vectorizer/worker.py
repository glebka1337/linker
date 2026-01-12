# src/workers/vectorizer/worker.py
from src.core.exceptions import NoteFoundError
from src.workers.base import BaseWorker
from src.schemas.note import LinkTask, VectorizeTask
from src.core.config import settings
import logging
from src.workers.vectorizer.deps import VectorWorkerDeps, assemble_vectorizer

class VectorWorker(BaseWorker[VectorizeTask, VectorWorkerDeps]):
    
    task_schema = VectorizeTask
    queue_name = settings.VECTORIZE_TASK_QUEUE_NAME
    assembler_funk=assemble_vectorizer

    def __init__(
        self
    ) -> None:
        super().__init__()
        
    async def process_task(
        self,
        task: VectorizeTask,
    ):
        # get a note text
        if not self.deps:
            msg = f"Dependencies were not assembled for class: {self.__class__.__name__}!"
            self.logger.error(msg)
            raise RuntimeError(msg)
        
        
        note = await self.deps.note_repo.get_by_uuid(
            task.note_uuid,
            owner_uuid=task.owner_uuid
        )
        
        if not note:
            raise NoteFoundError(f"Note not found: uuid={task.note_uuid}")
        
        self.logger.info(f"Turn note {task.note_uuid} to vector...")
        
        vec = await self.deps.ml_gateway.vectorize(
            text=note.text
        )
        
        # upsert created vector
        
        await self.deps.vector_repo.upsert(
            note_uuid=task.note_uuid,
            vector=vec
        )
        
        # create a task
        await self.deps.queue_service.send_msg(
            msg=LinkTask(
                note_uuid=task.note_uuid,
                vector=vec,
                owner_uuid=task.owner_uuid
            ),
            queue_name=settings.LINK_TASK_QUEUE_NAME
        )
        
        self.logger.info(f"Link task has been created and sent to the queue.")
        return
        
        
    