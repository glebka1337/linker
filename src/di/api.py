from fastapi import Request
from src.core.resources import Resources
from src.schemas.note import VectorizeTask
from src.core.config import settings
from src.models.note import Note as NoteDoc
from src.usecases.create_note import CreateNoteUseCase
from src.repos.mongo_repo import MongoRepo
from src.services.queue_service import RabbitQueueService
from src.services.vectorizer import Vectorizer

async def get_create_note_usecase(
    request: Request
) -> CreateNoteUseCase: # type: ignore
    # We need a repo for notes and vectorize interface
    resources: Resources = request.app.state.resources
    note_repo = MongoRepo(model=NoteDoc)
    
    # To use vectorizer, we need a queue
    
    queue = RabbitQueueService(conn=resources.rabbitmq_conn)
    
    vectorizer = Vectorizer(
        queue=queue,
        queue_name=settings.VECTORIZE_TASK_QUEUE_NAME,
        task_type=VectorizeTask
    )
    
    # Create usecase
    
    usecase = CreateNoteUseCase(
        repo=note_repo,
        vectorizer=vectorizer
    )
    
    return usecase