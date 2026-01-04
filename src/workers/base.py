from abc import ABC, abstractmethod
import logging
from src.core.resources import Resources, app_resource_manager
from typing import TypeVar, Generic, Type
from pydantic import BaseModel

TaskSchemaType = TypeVar("TaskSchemaType", bound=BaseModel)

class BaseWorker(ABC, Generic[TaskSchemaType]):
    
    queue_name: str
    task_schema: Type[TaskSchemaType]
    
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    async def process_task(
        self,
        task: TaskSchemaType,
        resources: Resources
    ): ...
    
    async def run(
        self
    ):
        async with app_resource_manager() as res:
            
            self.logger.info("Connecting via channel to queue...")
            
            async with res.rabbitmq_client.channel() as ch:
                await ch.set_qos(prefetch_count=1)
                
                que = await ch.declare_queue(
                    self.queue_name,
                    durable=True
                )
                
                self.logger.info("Start consuming messages")
                
                async with que.iterator() as que_iter:
                    async for msg in que_iter:
                        async with msg.process():
                            
                            self.logger.info(f"Starting proccessing of a task f{msg.message_id}")
                            
                            try:
                              task = self.task_schema.model_validate_json(
                                  msg.body
                              )
                              
                              await self.process_task(
                                  task, 
                                  resources=res
                              )
                            except Exception as e:
                              self.logger.error("Error during decoding task occured: %s" % e)
                              raise e