from src.repos.note_mongo_repo import NoteMongoRepo
from src.usecases.get_all_notes_usecase import GetAllNotesUseCase

async def get_all_notes_usecase() -> GetAllNotesUseCase:
    repo = NoteMongoRepo()
    return GetAllNotesUseCase(repo=repo)