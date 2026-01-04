from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from contextlib import asynccontextmanager
import logging

from src.models.note import Note

logger = logging.getLogger(__name__)

def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        settings.MONGO_DB_URL,
        maxPoolSize=100,
        minPoolSize=10,
        uuidRepresentation="standard"
    )
    
@asynccontextmanager
async def mongo_beanie_manager():
    
    mongo_client = get_mongo_client()
    
    try:
      
      await mongo_client.server_info()
      
      logger.info("Start initing beanie...")
      
      await init_beanie(
          database=mongo_client[settings.DB_NAME], # type: ignore
          document_models=[
              Note
          ]
      )
      
      yield mongo_client
      
      
    except Exception as e:
        logger.error(f"Error during mongo-beanie init occured: {e}")
        
    finally:
        mongo_client.close()
        logger.info("Closing mongo connection...")
        