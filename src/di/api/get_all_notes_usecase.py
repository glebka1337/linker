from src.repos.note_mongo_repo import NoteMongoRepo
from src.usecases.note.get_all_notes import GetAllNotesUseCase

async def get_all_notes_usecase() -> GetAllNotesUseCase:
    repo = NoteMongoRepo()
    return GetAllNotesUseCase(repo=repo)