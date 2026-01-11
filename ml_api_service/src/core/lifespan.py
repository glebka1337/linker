from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv, find_dotenv
from ml_api_service.src.utils import ensure_model_exists
from ml_api_service.src import ml_service as ml_service_module

find_dotenv()
load_dotenv()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info(f"Loadin model if not exists...")
    
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        model_name = os.getenv("ML_MODEL_NAME", 'sentence-transformers/all-MiniLM-L6-v2')
        model_path = BASE_DIR / 'ml_models'
        
        ensure_model_exists(
            model_name=model_name,
            model_path=model_path
        )
        
        # Create ml model service
        
        logger.info(f"Creating ML model service")
        service = ml_service_module.MLService(
            model_name=model_name,
            model_path=model_path
        )
        await service.load_model()
        
        ml_service_module.ml_service = service
        
    except Exception as e:
        logger.critical(f"Error during loading model: {e}")
        raise e
    
    yield
    