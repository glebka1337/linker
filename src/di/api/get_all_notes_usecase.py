from src.models.note import Note as NoteDoc
from src.repos.mongo_repo import MongoRepo
from src.usecases.get_all_notes_usecase import GetAllNotesUseCase

async def get_all_notes_usecase() -> GetAllNotesUseCase:
    repo = MongoRepo(model=NoteDoc)
    return GetAllNotesUseCase(repo=repo)