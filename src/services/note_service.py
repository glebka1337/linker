# src/services/note_service.py
from src.core.config import settings
from src.core.entities.note import NoteEntity
from src.core.exceptions import NoteFoundError
from src.interfaces.note_repo_interface import NoteRepo
from src.interfaces.queue_interface import QueueInterface
from src.schemas.note import NoteCreate, NoteUpdate, VectorizeTask
from src.services.queue_service import QueueService
from beanie.operators import In
import logging

logger = logging.getLogger(__name__)

class NoteService:

    def __init__(
        self,
        queue: QueueInterface,
        repo: NoteRepo
    ) -> None:
        self.queue: QueueInterface = queue
        self.repo: NoteRepo = repo
            
    async def create_note(
        self,
        note_data: NoteCreate
    ) -> NoteEntity:
        
        """
        Creates a new note in the database.

        Args:
            note_data (NoteCreate): The note data to be saved.

        Returns:
            NoteEntity: The saved note entity.

        Notes:
            After saving the note, a vectorize task is sent to the vectorize task queue.
        """
        note = NoteEntity(
            title=note_data.title,
            text=note_data.text
        )
        
        saved_note = await self.repo.create(
            note
        )
        
        logging.info(f"Note with {note.uuid} was successfyly added to MongoDB")
        
        # Add vectorize task to a queue
        
        logger.info("Send vectorize task...")
        
        await self.queue.send_msg(
            msg=VectorizeTask(
                note_uuid=note.uuid,
            ),
            queue_name=settings.VECTORIZE_TASK_QUEUE_NAME
        )
        
        return note
            
    async def get_all_notes(self) -> list[NoteEntity]:
        """
        Retrieves all notes from the database.

        Returns:
            List[Note]: A list of all the notes in the database.
        """
        return await self.repo.get_all()
    
    async def get_note_by_uuid(
        self,
        note_uuid: str
    ) -> NoteEntity | None:
        """
        Searhes for note, if exists -> returns it, if not raises exception

        Args:
            note_uuid (str): UUID od a note

        Returns:
            NoteEntity | None: _description_
        """
        
        note: NoteEntity | None = await self.repo.get_by_uuid(
            note_uuid=note_uuid
        )
        
        if not note:
            raise NoteFoundError(f"Note with uuid: {note_uuid} was not found")
        
        return note
    
    async def get_notes_by_uuids(
        self,
        main_note_uuid: str,
        lim: int | None = None
    ): 
        note = await self.repo.get_by_uuid(
            note_uuid=main_note_uuid
        )
        
        if not note:
            # That is an exception, it should not act in that way
            err_msg = f"Note was not found: uuid={main_note_uuid}"
            logger.error(err_msg)
            raise NoteFoundError(
                err_msg
            )
        
        # Get related notes
        
        return await self.repo.get_by_uuids(
            uuids=[n.note_uuid for n in note.related_notes], lim=lim
        )
        
        
    async def update_note(
        self,
        note_data: NoteUpdate,
        note_uuid: str
    ) -> NoteEntity:
        
        note = await self.repo.get_by_uuid(
            note_uuid=note_uuid
        )
        
        if not note:
            # exception - not found
            err_msg = f"Note was not found: uuid={note_uuid}"
            logger.error(err_msg)
            raise NoteFoundError(
                err_msg
            )

        changes = note.model_dump(
            exclude_unset=True
        )
        
        if not changes:
            return note

        curr_note_updated = note.model_copy(update=changes)
        
        curr_note_updated.related_notes = []
        
        updated = await self.repo.update(
            curr_note_updated
        )
        
        if not updated:
            msg = f"Error updating a note with uuid={note.uuid}"
            logger.error(msg)
            raise NoteFoundError(
                msg
            )
        
        logger.info(f"Note {note.uuid} was updated, creating task for vectorization")
        
        await self.queue.send_msg(
            msg=VectorizeTask(
                note_uuid=updated.uuid,
            ),
            queue_name=settings.VECTORIZE_TASK_QUEUE_NAME
        )
        
        return updated
        
