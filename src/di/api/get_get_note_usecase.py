from src.repos.note_mongo_repo import NoteMongoRepo
from src.usecases.note.get_note import GetNoteUseCase


async def get_get_note_usecase() -> GetNoteUseCase:
    
    repo = NoteMongoRepo()
    
    return GetNoteUseCase(repo=repo)