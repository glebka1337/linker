# src/db/rabbit.py
import aio_pika
from contextlib import asynccontextmanager
from src.core.config import settings
async def create_queue_connection() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(
        url=settings.RABBITMQ_URL
    )
    
@asynccontextmanager
async def rabbitmq_conn_manager():
    conn = await create_queue_connection()
    try:
      yield conn
    finally:
      await conn.close()