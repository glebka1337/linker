from pathlib import Path
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from typing import ClassVar

class Settings(BaseSettings):
    # general
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parent.parent.parent
    
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = 'localhost'
    DB_PORT: int = 27017
    
    QDRANT_HOST: str = 'localhost' # TODO: Change when app is in docker
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "note_vector_collection"
    
    # Rabbitmq settings
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str = 'localhost'
    
    # Queue settings
    VECTORIZE_TASK_QUEUE_NAME: str = 'vectorize_tasks'
    LINK_TASK_QUEUE_NAME: str = 'link_tasks'
    
    # Model config
    ML_MODEL_NAME: str = 'sentence-transformers/all-MiniLM-L6-v2'
    ML_MODEL_DIR_PATH: ClassVar[Path] = BASE_DIR / 'ml_models'
    ML_SERVICE_URL: str = 'http://localhost:8000'
    
    @property
    def MONGO_DB_URL(self):
        return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?authSource=admin"
    
    @property
    def QDRANT_DB_URL(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"
    
    @property
    def RABBITMQ_URL(self): # amqp://user:pass@host:port
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_HOST}:5672/"
    
    @property
    def ML_MODEL_PATH(self):
        return self.ML_MODEL_DIR_PATH / self.ML_MODEL_NAME.split('/')[-1]
    
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings() # type: ignore