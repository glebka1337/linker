from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from src.di.api import get_create_note_usecase
from src.schemas.note import NoteCreate
from src.usecases.create_note import CreateNoteUseCase

rt = APIRouter(
    tags=["notes", "main"]
)

@rt.post('/')
async def create_note(
    note_data: NoteCreate,
    create_note_usecase: CreateNoteUseCase = Depends(get_create_note_usecase),
):
    try:
      await create_note_usecase.execute(note_data)
    except Exception as e:
      raise HTTPException(detail="Error occured: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@rt.get('/{note_uuid}')
async def get_note(
    note_uuid: str,
    get_note_usecase: ...
): ...