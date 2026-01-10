from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from ml_api_service.src.core.config import settings
from ml_api_service.src.utils import ensure_model_exists
from ml_api_service.src import ml_service as ml_service_module

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info(f"Loadin model if not exists...")
    
    try:
        
        ensure_model_exists(
            model_name=settings.ML_MODEL_NAME,
            model_path=settings.ML_MODEL_DIR_PATH
        )
        
        # Create ml model service
        
        logger.info(f"Creating ML model service")
        
        service = ml_service_module.MLService(
            model_name=settings.ML_MODEL_NAME,
            model_path=settings.ML_MODEL_DIR_PATH
        )
        await service.load_model()
        
        ml_service_module.ml_service = service
        
    except Exception as e:
        logger.critical(f"Error during loading model: {e}")
        raise e
    
    yield
    