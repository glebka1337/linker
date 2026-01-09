# src/workers/base.py
from abc import ABC, abstractmethod
import logging
from typing import Awaitable, Callable, ClassVar, Protocol, TypeVar, Generic, Type
from pydantic import BaseModel
from src.core.resources import Resources, app_resource_manager


DepsType = TypeVar("DepsType", covariant=True)
TaskSchemaType = TypeVar("TaskSchemaType", bound=BaseModel)

AssemblerFunc = Callable[[Resources], Awaitable[DepsType]]

class BaseWorker(ABC, Generic[TaskSchemaType, DepsType]):
    
    queue_name: str
    task_schema: Type[TaskSchemaType]
    assembler_funk: ClassVar[AssemblerFunc]
    
    def __init__(
        self
    ) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__
        )
        self.deps: DepsType | None = None
    
    def __init_subclass__(cls) -> None:
        
        required_fields = ['queue_name', 'task_schema', 'assembler_funk']
        cls_name = cls.__name__
        for f in required_fields:
            if not hasattr(cls, f):
                raise TypeError(f"Class {cls_name} forgot to define field: {f}")
    
    @abstractmethod
    async def process_task(
        self,
        task: TaskSchemaType
    ): ...
    
    async def setup(
        self,
        res: Resources
    ):
        cls_name = self.__class__.__name__
        self.logger.info(f"Start assembling deps {cls_name}...")
        self.deps = await self.__class__.assembler_funk(res)
        
        self.logger.info(f"Ended succesfully")
        
    async def run(
        self,
        resources: Resources
    ):
            
        self.logger.info("Connecting via channel to queue...")
    
        
        await self.setup(resources)
        rabbitmq_conn = resources.rabbitmq_conn
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