from typing import (
    Optional,
    Annotated
)
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Query
)
from src.core.exceptions import NoteFoundError
from src.schemas.note import NoteCreate, NoteRead, NoteUpdate
from src.services.note_service import NoteService

rt = APIRouter(
    tags=["notes", "main"]
)

@rt.post(
    '/',
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED
)
async def create_note(
    note_data: NoteCreate
):
    return await NoteService.create_note(
        note_data
    )
    
@rt.get(
    '/',
    tags=['notes'],
    response_model=list[NoteRead],
)
async def get_all_notes():
    return await NoteService.get_all_notes()

@rt.get(
    '/{note_uuid}',
    response_model = NoteRead
)
async def get_note_by_uuid(
    note_uuid: str,
):
    try:
        return await NoteService.get_note_by_uuid(
            note_uuid=note_uuid
        )
    except NoteFoundError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_404_NOT_FOUND
        )
    

@rt.get(
    '/{note_uuid}/related_notes',
    response_model = list[NoteRead]
)
async def get_related_notes(
    note_uuid: str,
    lim: Annotated[int | None, Query(le=100, description="Limit to retrieve")] = None
):
    return await NoteService.get_notes_by_uuids(
        main_note_uuid=note_uuid, lim=lim if lim else None
    )

@rt.patch(
    '/{note_uuid}'
)
async def update_note(
    note_uuid: str,
    note_data: NoteUpdate
): 
    ...
    
    