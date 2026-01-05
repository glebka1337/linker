from src.core.resources import Resources
from src.repos.vector_repo import QdrantVectorRepo
from src.workers.base import BaseWorker
from src.schemas.note import LinkTask
from src.core.config import settings

class LinkerWorker(BaseWorker[LinkTask]):
    
    task_schema = LinkTask
    queue_name = settings.LINK_TASK_QUEUE_NAME
    
    def __init__(self) -> None:
        super().__init__()
    
    async def setup(self, res: Resources):
        
        ...
    
    async def process_task(
        self,
        task: LinkTask
    ):
        ...
    