import logging
from src.interfaces.note_repo_interface import NoteRepo

logger = logging.getLogger(__name__)

class GetAllNotesUseCase:
    def __init__(self, repo: NoteRepo):
        self.repo = repo

    async def execute(self):
        logger.info("Fetching all notes from database")
        return await self.repo.get_all()