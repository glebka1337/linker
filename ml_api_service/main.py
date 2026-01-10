from fastapi import FastAPI
from ml_api_service.src.router import rt as main_router
from ml_api_service.src.core.lifespan import lifespan

app = FastAPI(title="ML Service for embedings", lifespan=lifespan)

app.include_router(main_router, prefix='/api/v1/')