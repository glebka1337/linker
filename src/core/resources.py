from pydantic import BaseModel
from typing import Optional
from qdrant_client import AsyncQdrantClient
from motor.motor_asyncio import AsyncIOMotorClient
from aio_pika.abc import AbstractRobustConnection

class Resources(BaseModel):
    qdrant_client: Optional[AsyncQdrantClient] = None
    mongo_client: Optional[AsyncIOMotorClient] = None
    rabbitmq_conn: Optional[AbstractRobustConnection] = None