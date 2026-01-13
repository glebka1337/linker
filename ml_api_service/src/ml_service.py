# ml_api_service/ml_service.py
from pathlib import Path
from sentence_transformers import SentenceTransformer
import asyncio
import logging

logger = logging.getLogger(__name__)

class MLService:
    
    def __init__(
        self,
        model_name: str,
        model_path: Path
    ) -> None:    
        self.model: None | SentenceTransformer = None
        self.model_name: str = model_name
        self.model_path: Path = model_path
       
    async def load_model(
        self
    ):  
        try:
            logger.info(f"Loading model {self.model_name} from {self.model_path}...")
            self.model = await asyncio.to_thread(SentenceTransformer, str(self.model_path))
            
        except Exception as e:
            logger.critical(f"Problem during loadin model occured: {e}")
            raise e

    async def vectorize(
        self,
        text: str
    ) -> list[float]:
        
        if not self.model:
            raise RuntimeError("Model was not loaded!")
        
        vec = await asyncio.to_thread(
            self.model.encode,  # pyright: ignore[reportOptionalMemberAccess]
            text
        )
        
        return vec.tolist()

ml_service: MLService | None = None

async def get_ml_service() -> MLService:
    global ml_service
    
    if not ml_service:
        raise RuntimeError("ML service was not created!")
    
    return ml_service
    