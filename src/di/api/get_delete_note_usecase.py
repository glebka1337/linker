from src.repos.note_mongo_repo import NoteMongoRepo
from src.usecases.delete_note_usecase import DeleteNoteUseCase

async def get_delete_note_usecase() -> DeleteNoteUseCase:
    repo = NoteMongoRepo()
    return DeleteNoteUseCase(repo=repo)