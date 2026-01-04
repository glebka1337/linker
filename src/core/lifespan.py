from contextlib import asynccontextmanager
from rich.console import Console
from fastapi import FastAPI
from src.db.mongo import (
    init_mongo,
    close_mongo
)
from src.services.queue_service import QueueService

console = Console()
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        with console.status(
            "[bold yellow]Establishing MongoDB connection...",
            spinner="dots",
        ):
            await init_mongo()
        
        console.print(
            "Connection established successfully!",
            style="green"
        )
        
    except Exception as e:
        console.print("Mongo failed to start: %s" % e, style="red bold")
        raise 
    
    console.print("Connecting to queue...", style="bold yellow")
    
    yield 
    
    with console.status(
        "[yellow italic]Closing MongoDB[/yellow italic]",
        spinner="line"
    ):
        await close_mongo()
    