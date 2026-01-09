from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.logger import setup_logging
from src.core.resources import Resources
from src.db.qdrant import qdrant_client_manager
from src.db.mongo import mongo_beanie_manager
from src.db.rabbit import rabbitmq_conn_manager

import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    setup_logging()
        
    logger = logging.getLogger(__name__)
    
    logger.info(f"Creating all app resources.")
    try:

        async with (
            mongo_beanie_manager() as mongo_client,
            rabbitmq_conn_manager() as rabbitmq_conn
        ):
            resources = Resources(
                mongo_client=mongo_client,
                rabbitmq_conn=rabbitmq_conn
            )
            
            app.state.resources = resources
            yield
            logger.info(f"Closing all posible connection, clients...")
        
    except Exception as e:
        logger.critical(f"Error occured in a lifespan: {e}")
        raise e
    