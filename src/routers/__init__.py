from fastapi import FastAPI
from .note_router import rt as note_router

def init_routers(app: FastAPI):
    app.include_router(note_router, prefix='/notes')