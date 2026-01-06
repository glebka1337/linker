# src/workers/base.py
from abc import ABC, abstractmethod
import logging
from typing import Awaitable, Callable, Protocol, TypeVar, Generic, Type
from pydantic import BaseModel
from src.core.resources import Resources, app_resource_manager


DepsType = TypeVar("DepsType", covariant=True)
TaskSchemaType = TypeVar("TaskSchemaType", bound=BaseModel)

AssemblerFunc = Callable[[Resources], Awaitable[DepsType]]

class BaseWorker(ABC, Generic[TaskSchemaType, DepsType]):
    
    queue_name: str
    task_schema: Type[TaskSchemaType]
    
    def __init__(
        self,
        assembler_funk: AssemblerFunc
    ) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__
        )
        self.assembler_funk = assembler_funk
        self.deps: DepsType | None = None
        
    @abstractmethod
    async def process_task(
        self,
        task: TaskSchemaType
    ): ...
    
    async def setup(
        self,
        res: Resources
    ):
        self.logger.info(f"Start assembling deps...")
        self.deps = await self.assembler_funk(res)
        
        self.logger.info(f"Ended succesfully")
        
    async def run(
        self
    ):
            
        self.logger.info("Connecting via channel to queue...")
        async with app_resource_manager() as res:
            
            await self.setup(res)
            rabbitmq_conn = res.rabbitmq_conn
            async with rabbitmq_conn.channel() as ch:
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
                                )
                            except Exception as e:
                                self.logger.error("Error during decoding task occured: %s" % e)
                                raise e