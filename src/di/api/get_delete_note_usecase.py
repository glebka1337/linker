from src.repos.note_mongo_repo import NoteMongoRepo
from src.usecases.note.delete_note import DeleteNoteUseCase

async def get_delete_note_usecase() -> DeleteNoteUseCase:
    repo = NoteMongoRepo()
    return DeleteNoteUseCase(repo=repo)