# src/core/logger.py
from rich.logging import RichHandler
import logging

def setup_logging():
    
    handlers = [
        RichHandler(
            show_time=True,
            show_level=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True
        )
    ]
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=handlers
    )
    
    