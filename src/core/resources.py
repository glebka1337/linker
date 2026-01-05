# src/core/resorces.py
from contextlib import asynccontextmanager
from dataclasses import dataclass
from qdrant_client import AsyncQdrantClient
from motor.motor_asyncio import AsyncIOMotorClient
from aio_pika.abc import AbstractRobustConnection
from src.db.mongo import mongo_beanie_manager
from src.db.qdrant import qdrant_client_manager
from src.db.rabbit import rabbitmq_conn_manager

import logging

logger = logging.getLogger(__name__)

@dataclass
class Resources:
    qdrant_client: AsyncQdrantClient
    mongo_client: AsyncIOMotorClient
    rabbitmq_conn: AbstractRobustConnection

@asynccontextmanager
async def app_resource_manager():

    async with (
        qdrant_client_manager() as qdrant,
        mongo_beanie_manager() as mongo,
        rabbitmq_conn_manager() as rabbitmq
    ):
        
        logger.info("All resorces initialized!")
        yield Resources(
            qdrant_client=qdrant,
            mongo_client=mongo,
            rabbitmq_conn=rabbitmq
        )
    logger.info("Closing all possible connections...")
    
      
    