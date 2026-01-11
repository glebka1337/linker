from src.models.note import Note as NoteDoc
from src.repos.mongo_repo import MongoRepo
from src.usecases.get_note_usecase import GetNoteUseCase


async def get_get_note_usecase() -> GetNoteUseCase:
    
    repo = MongoRepo(
        model=NoteDoc
    )
    
    return GetNoteUseCase(repo=repo)