import logging
from src.interfaces.note_repo_interface import NoteRepo

logger = logging.getLogger(__name__)

class DeleteNoteUseCase:
    
    def __init__(
        self,
        repo: NoteRepo
    ) -> None:
        self.repo = repo
    
    async def execute(
        self,
        note_uuid: str
    ) -> bool:
        
        """
        Returns boolean - is deleted or not
        """
        # check if note exists
        note = await self.repo.get_by_uuid(
            note_uuid
        )
        
        if not note:
            logger.info(f'Note {note_uuid} was not found to be deleted')
            return False
        
        # delete note
        
        is_deleted = await self.repo.delete(
            note_uuid
        )
        
        if not is_deleted:
            logger.warning(f'Note {note_uuid} was not deleted')
            return False

        # delete related links
        
        await self.repo.remove_related_links(
            targer_uuid=note_uuid
        )
        
        return True
        