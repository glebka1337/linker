from fastapi import FastAPI
from src.core.lifespan import lifespan
from src.routers import init_routers
from src.core.logger import setup_logging

setup_logging()

app = FastAPI(
    lifespan=lifespan
)
init_routers(app)

@app.get(
    '/health'
)
async def health():
    return {
        "status": 200
    }