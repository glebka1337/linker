# src/services/queue_service_02.py
import aio_pika
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class RabbitQueueService:
    
    def __init__(
        self,
        conn: aio_pika.abc.AbstractRobustConnection
    ) -> None:
        self.conn = conn
        
    async def send_msg(
        self,
        msg: BaseModel,
        queue_name: str
    ) -> None:
        try:
            async with self.conn.channel() as ch:
                queue = await ch.declare_queue(
                    queue_name,
                    durable=True
                )
                
                body = msg.model_dump_json().encode()
                
                message = aio_pika.Message(
                    body=body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                )
                
                await ch.default_exchange.publish(
                    message=message,
                    routing_key=queue_name
                )
                logger.info(f"Sended message to {queue_name}")
        except Exception as e:
            logger.error(f"Error occured: {e}")
            raise e
            