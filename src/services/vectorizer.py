# src/services/vectorizer.py
from pydantic import BaseModel
from src.interfaces.queue_interface import QueueServiceInterface
from typing import Generic, Type, TypeVar

TaskType = TypeVar("TaskType", bound=BaseModel)

class Vectorizer(Generic[TaskType]):
    """
    Class is an implementation of VectorizerInterface
    Responsible for sending a messages for vectorization
    """ 
    
    def __init__(
        self,
        queue: QueueServiceInterface,
        queue_name: str,
        task_type: Type[TaskType]
    ) -> None:
        self.queue = queue
        self.queue_name = queue_name
        self.task_type = task_type
        
    async def send_for_process(
        self,
        note_uuid: str
    ) -> None:
        task = self.task_type(note_uuid=note_uuid)
        
        await self.queue.send_msg(
            msg=task,
            queue_name=self.queue_name
        )
        