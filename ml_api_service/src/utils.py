# ml_api_service/src/utils.py
from pathlib import Path
import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

def ensure_model_exists(
    model_path: Path,
    model_name: str
):
    if not model_path.exists():
        
        logger.info("Downloading a model...")
        
        try:
            model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Error occured during downloding a model: %s" % e)
            raise e

        logger.info(f"Saving model to the path: {str(model_path)}")
        
        model_path.mkdir(exist_ok=True, parents=True)
        
        model.save(path=str(model_path))
        logger.info("Model has been successfuly saved")
    else:
        logger.info("Model exists")
        