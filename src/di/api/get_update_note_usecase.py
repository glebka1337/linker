from fastapi import Depends
from aio_pika.abc import AbstractRobustConnection
from src.models.note import Note as NoteDoc
from src.repos.mongo_repo import MongoRepo
from src.services.queue_service import RabbitQueueService
from src.usecases.update_note_usecase import UpdateNoteUseCase
from src.di.rabbit import get_rabbitmq_connection 

async def get_update_note_usecase(
    conn: AbstractRobustConnection = Depends(get_rabbitmq_connection)
) -> UpdateNoteUseCase:
    
    repo = MongoRepo(
        model=NoteDoc
    )
    
    queue_service = RabbitQueueService(conn=conn)
    
    return UpdateNoteUseCase(
        repo=repo,
        queue=queue_service
    )