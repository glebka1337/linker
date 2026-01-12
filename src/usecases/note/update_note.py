import logging
from src.interfaces.note_repo_interface import NoteRepo
from src.core.config import settings
from src.interfaces.queue_interface import QueueServiceInterface 
from src.schemas.note import NoteRead, NoteUpdate, VectorizeTask

logger = logging.getLogger(__name__)

class UpdateNoteUseCase:
    
    def __init__(
        self,
        repo: NoteRepo,
        queue: QueueServiceInterface    
    ) -> None:
        self.repo = repo
        self.queue = queue
        
    async def execute(
        self,
        note_uuid: str,
        owner_uuid: str,
        note_data: NoteUpdate,
        
    ) -> NoteRead | None:
        
        existing_note = await self.repo.get_by_uuid(
            owner_uuid=owner_uuid,
            note_uuid=note_uuid
        )
        
        if not existing_note:
            return None

        text_changed = False

        if note_data.title is not None and note_data.title != existing_note.title:
            existing_note.title = note_data.title

        if note_data.text is not None and note_data.text != existing_note.text:
            existing_note.text = note_data.text
            text_changed = True

        updated_note = await self.repo.update(existing_note, owner_uuid=owner_uuid)
        
        if not updated_note:
            return None

        if text_changed:
            logger.info(f"Text changed for note {note_uuid}. Sending task to queue.")
            
            task = VectorizeTask(
                note_uuid=note_uuid,
                force_update=True,
                owner_uuid=owner_uuid
            )
            
            await self.queue.send_msg(
                msg=task,
                queue_name=settings.VECTORIZE_TASK_QUEUE_NAME
            )

        return NoteRead(
            uuid=updated_note.uuid,
            title=updated_note.title,
            text=updated_note.text,
            created_at=updated_note.created_at,
            related_notes=[]
        )