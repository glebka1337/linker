import logging
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from src.di.api.get_delete_note_usecase import get_delete_note_usecase
from src.di.api.get_update_note_usecase import get_update_note_usecase
from src.di.api.get_get_note_usecase import get_get_note_usecase
from src.di.api.get_create_note_usecase import get_create_note_usecase
from src.schemas.note import NoteCreate, NoteRead, NoteUpdate
from src.usecases.create_note_usecase import CreateNoteUseCase
from src.usecases.delete_note_usecase import DeleteNoteUseCase
from src.usecases.get_note_usecase import GetNoteUseCase
from src.usecases.update_note_usecase import UpdateNoteUseCase

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
        
@rt.patch('/{note_uuid}', response_model=NoteRead)
async def update_note(
    note_uuid: str,
    note_data: NoteUpdate,
    update_note_usecase: UpdateNoteUseCase = Depends(get_update_note_usecase)
):
    try:
        updated_note = await update_note_usecase.execute(note_uuid, note_data)
        
        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with uuid: {note_uuid} was not found"
            )
            
        return updated_note

    except HTTPException as he:
        raise he

    except Exception as e:
        logger.critical(f"Unexpected error in update_note: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
        
@rt.delete('/{note_uuid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_uuid: str,
    delete_usecase: DeleteNoteUseCase = Depends(get_delete_note_usecase)
):
    try:
        is_deleted = await delete_usecase.execute(note_uuid)
        
        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with uuid: {note_uuid} was not found"
            )
        
        # При 204 return не нужен, или просто return None
        return 

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.critical(f"Error deleting note: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )