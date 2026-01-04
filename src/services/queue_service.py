import json
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, Message
import aio_pika
from src.core.config import settings
from src.schemas.note import (
    VectorizeTask,
    LinkTask
)

class QueueService:
    _conn: AbstractRobustConnection = None # type: ignore
    
    @classmethod
    async def get_connection(cls) -> aio_pika.abc.AbstractRobustConnection:
        
        if cls._conn is None:
            cls._conn = await connect_robust(
                url=settings.RABBITMQ_URL
            )
            
        return cls._conn
        
    @classmethod
    async def close(cls):
        
        if cls._conn:
            await cls._conn.close()
    
    @classmethod
    async def send_msg(
        cls,
        data: VectorizeTask | LinkTask,
        queue_name: str
    ):
        
        _ = await cls.get_connection()
        
        async with cls._conn.channel() as ch:
            
            queue = await ch.declare_queue(
                name=queue_name,
                durable=True
            )
            
            await ch.default_exchange.publish(
                message=Message(
                    body=data.model_dump_json().encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue_name
            )

queue_service = QueueService()
            
            
            