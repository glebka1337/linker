from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.resources import app_resource_manager
from src.core.logger import setup_logging
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    setup_logging()
        
    logger = logging.getLogger(__name__)
    
    logger.info(f"Creating all app resources.")
    try:
        async with app_resource_manager() as resources:
            app.state.resources = resources
            yield
            logger.info(f"Closing all posible connection, clients...")
            
    except Exception as e:
        logger.critical(f"Error occured in a lifespan: {e}")
        raise e
    