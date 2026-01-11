from fastapi import FastAPI
import uvicorn
from ml_api_service.src.router import rt as main_router
from ml_api_service.src.core.lifespan import lifespan

app = FastAPI(title="ML Service for embedings", lifespan=lifespan)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)