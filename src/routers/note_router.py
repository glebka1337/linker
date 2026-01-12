import logging
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from src.di.auth import get_current_user_uuid 
from src.di.api.get_all_notes_usecase import get_all_notes_usecase
from src.di.api.get_delete_note_usecase import get_delete_note_usecase
from src.di.api.get_update_note_usecase import get_update_note_usecase
from src.di.api.get_get_note_usecase import get_get_note_usecase
from src.di.api.get_create_note_usecase import get_create_note_usecase
from src.schemas.note import NoteCreate, NoteRead, NoteShortRead, NoteUpdate
from src.usecases.note.get_all_notes import GetAllNotesUseCase
from src.usecases.note.create_note import CreateNoteUseCase
from src.usecases.note.delete_note import DeleteNoteUseCase
from src.usecases.note.get_note import GetNoteUseCase
from src.usecases.note.update_note import UpdateNoteUseCase

note_router = APIRouter(
    tags=["notes", "main"]
)

logger = logging.getLogger(__name__)

# --- CREATE ---
@note_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    owner_uuid: str = Depends(get_current_user_uuid), 
    create_note_usecase: CreateNoteUseCase = Depends(get_create_note_usecase),
):
    try:

        return await create_note_usecase.execute(note_data, owner_uuid)
    except Exception as e:
        logger.error(f"Error creating note: {e}", exc_info=True)
        raise HTTPException(
            detail="Error occured during note creation", 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  
# --- GET ONE ---
@note_router.get('/{note_uuid}', response_model=NoteRead)
async def get_note(
    note_uuid: str,
    owner_uuid: str = Depends(get_current_user_uuid), # <--- Замок
    get_note_usecase: GetNoteUseCase = Depends(get_get_note_usecase)
): 
    try:
        note = await get_note_usecase.execute(note_uuid, owner_uuid)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with uuid: {note_uuid} was not found"
            )
            
        return note
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.critical(f"Unexpected error getting note: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Oups! Error occured"
        )

# --- UPDATE ---
@note_router.patch('/{note_uuid}', response_model=NoteRead)
async def update_note(
    note_uuid: str,
    note_data: NoteUpdate,
    owner_uuid: str = Depends(get_current_user_uuid), # <--- Замок
    update_note_usecase: UpdateNoteUseCase = Depends(get_update_note_usecase)
):
    try:
        updated_note = await update_note_usecase.execute(
            note_uuid=note_uuid,
            note_data=note_data,
            owner_uuid=owner_uuid
        )
        
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

# --- DELETE ---
@note_router.delete('/{note_uuid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_uuid: str,
    owner_uuid: str = Depends(get_current_user_uuid), # <--- Замок
    delete_usecase: DeleteNoteUseCase = Depends(get_delete_note_usecase)
):
    try:
        is_deleted = await delete_usecase.execute(note_uuid, owner_uuid)
        
        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note with uuid: {note_uuid} was not found"
            )
        return 

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.critical(f"Error deleting note: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

# --- GET ALL ---
@note_router.get('/', response_model=list[NoteShortRead])
async def get_all_notes(
    owner_uuid: str = Depends(get_current_user_uuid), # <--- Замок
    usecase: GetAllNotesUseCase = Depends(get_all_notes_usecase)
):
    try:
        return await usecase.execute(owner_uuid)
    except Exception as e:
        logger.error(f"Failed to fetch notes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")