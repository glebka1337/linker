from src.core.entities.note import RelatedNoteEntity
from src.core.exceptions import NoteFoundError
from src.workers.base import BaseWorker
from src.schemas.note import LinkTask
from src.core.config import settings
from src.workers.linker.deps import LinkerDeps, assemble_linker

class LinkerWorker(BaseWorker[LinkTask, LinkerDeps]):
    
    task_schema = LinkTask
    queue_name = settings.LINK_TASK_QUEUE_NAME
    assembler_funk=assemble_linker
    
    def __init__(self) -> None:
        super().__init__()
    
    async def process_task(
        self,
        task: LinkTask
    ):
        if not self.deps:
            msg = f"Dependencies were not assembled for class: {self.__class__.__name__}!"
            self.logger.error(msg)
            raise RuntimeError(msg)
        
        # get a similiar vectors
        sim_vectors = await self.deps.vector_repo.search(
            vector=task.vector,
            excluded_note_uuid=task.note_uuid
        )
        
        if not sim_vectors:
            self.logger.info(f"No similar notes / vectors were found for{task.note_uuid}")
            return
        
        # if we found similar vectors, we need to update
        target_note = await self.deps.note_repo.get_by_uuid(
            note_uuid=task.note_uuid
        )
        
        if not target_note: # that is not expected behavior!
            raise NoteFoundError(f"Note with {task.note_uuid} were not found for further update")

        # update note
        target_note.related_notes = [
            RelatedNoteEntity(
                note_uuid=v.note_uuid,
                score=v.score
            )
            for v in sim_vectors
        ]
        
        await self.deps.note_repo.update(
            note=target_note
        )
        
        self.logger.info(f"Linking of a note (uuid:{task.note_uuid}) ended successfuly")
        
        
    