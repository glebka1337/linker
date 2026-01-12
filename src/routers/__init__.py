from fastapi import FastAPI
from .note_router import rt as note_router
from .auth_router import auth_router

def init_routers(app: FastAPI):
    app.include_router(note_router, prefix='/notes')
    app.include_router(auth_router, prefix='/auth')