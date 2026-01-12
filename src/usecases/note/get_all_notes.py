import logging
from src.interfaces.note_repo_interface import NoteRepo

logger = logging.getLogger(__name__)

class GetAllNotesUseCase:
    def __init__(self, repo: NoteRepo):
        self.repo = repo

    async def execute(self, owner_uuid: str):
        logger.info("Fetching all notes from database")
        return await self.repo.get_all(owner_uuid)