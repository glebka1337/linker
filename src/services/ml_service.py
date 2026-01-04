# src/services/ml_service.py
from pathlib import Path
from sentence_transformers import SentenceTransformer
import asyncio
import logging

logger = logging.getLogger(__name__)

class MLService:
    
    def __init__(
        self,
        model_name: str,
        model_path: Path,
    ) -> None:
        self.model: None | SentenceTransformer = None
        self.models_name: str = model_name
        self.model_path: Path = model_path
    
    async def init_model(
        self,
    ) -> None:
        path = self.model_path
        
        if not path.exists():
            
            logger.info("Downloading a model...")
            
            try:
                
                self.model = await asyncio.to_thread(
                    SentenceTransformer,
                    self.models_name
                )
                
            except Exception as e:
                logger.error(f"Error occured during downloding a model: %s" % e)
                raise e

            logger.info(f"Saving model to the path: {str(path)}")
            
            path.mkdir(exist_ok=True, parents=True)
            
            self.model.save(path=str(path))
            logger.info("Model has been successfuly saved")
            
        else:
            logger.info("Model exists, loading")
            self.model = await asyncio.to_thread(
                SentenceTransformer,
                str(self.model_path)
            )
                
    async def vectorize(
        self,
        text: str
    ) -> list[float]:
        
        if not self.model:
            await self.init_model()
        
        vec = await asyncio.to_thread(
            self.model.encode,  # pyright: ignore[reportOptionalMemberAccess]
            text
        )
        
        return vec.tolist()
        