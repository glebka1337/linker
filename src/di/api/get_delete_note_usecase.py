from src.models.note import Note as NoteDoc
from src.repos.mongo_repo import MongoRepo
from src.usecases.delete_note_usecase import DeleteNoteUseCase

async def get_delete_note_usecase() -> DeleteNoteUseCase:
    repo = MongoRepo(
        model=NoteDoc
    )
    return DeleteNoteUseCase(repo=repo)