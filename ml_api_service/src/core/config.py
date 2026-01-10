from pathlib import Path
from typing import ClassVar
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    ML_MODEL_NAME: str = 'sentence-transformers/all-MiniLM-L6-v2'
    ML_MODEL_DIR_PATH: ClassVar[Path] = BASE_DIR / 'ml_models'

settings = Settings()

