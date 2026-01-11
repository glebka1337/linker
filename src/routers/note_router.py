import logging
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from src.di.api.get_get_note_usecase import get_get_note_usecase
from src.di.api.get_create_note_usecase import get_create_note_usecase
from src.schemas.note import NoteCreate, NoteRead
from src.usecases.create_note import CreateNoteUseCase
from src.usecases.get_note_usecase import GetNoteUseCase

rt = APIRouter(
    tags=["notes", "main"]
)

logger = logging.getLogger(__name__)

@rt.post('/')
async def create_note(
    note_data: NoteCreate,
    create_note_usecase: CreateNoteUseCase = Depends(get_create_note_usecase),
):
    try:
        await create_note_usecase.execute(note_data)
    except Exception as e:
        raise HTTPException(detail="Error occured: {e}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@rt.get('/{note_uuid}', response_model=NoteRead)
async def get_note(
    note_uuid: str,
    get_note_usecase: GetNoteUseCase = Depends(get_get_note_usecase)
): 
    try:
        note = await get_note_usecase.execute(note_uuid)
        if not note:
            raise HTTPException(
                404,
                f"Note with uuid: {note_uuid} was not found"
            )
            
        return note
    except HTTPException as he:
        raise he

    except Exception as e:
        logger.critical(f"Unexpected error occured: {e}")
        raise HTTPException(
            500,
            "Oups! Error occured"
        )