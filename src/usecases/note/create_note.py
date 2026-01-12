# src/usecases/create_note.py
from src.core.entities.note import NoteEntity
from src.interfaces.note_repo_interface import NoteRepo
from src.interfaces.vectorizer_interface import VectorizerInterface
import logging
from src.schemas.note import NoteCreate

logger = logging.getLogger(__name__)

class CreateNoteUseCase:
    
    def __init__(
        self,
        repo: NoteRepo,
        vectorizer: VectorizerInterface
    ) -> None:
        self.repo = repo
        self.vectorizer = vectorizer
        
    async def execute(
        self,
        note_data: NoteCreate,
        owner_uuid: str
    ) -> NoteEntity: 
        
        note = NoteEntity(
            title=note_data.title,
            text=note_data.text,
            owner_uuid=owner_uuid
        )
        
        logger.info(f"Started 'create note' use case...")
        
        note_created = await self.repo.create(
            note_data=note
        )
        
        logger.info(f"Sending a message for vectorization")
        
        try:
            
            await self.vectorizer.send_for_process(
                note_uuid=note_created.uuid
            )
        
        except Exception as e:
            logger.error(f"Error during sending a message occured: {e}")    
        
        return note_created