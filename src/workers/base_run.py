# src/workers/base_run.py
import sys
import asyncio
import logging
from typing import TypeVar, Type
from src.core.logger import setup_logging
from src.workers.base import BaseWorker

WorkerType = TypeVar("WorkerType", bound=BaseWorker)

async def run_worker(
    WorkerClass: Type[BaseWorker]
):
    setup_logging()
    cls_name = WorkerClass.__name__
    run_logger = logging.getLogger(f"Runner: {cls_name}")
    
    try:
        run_logger.info("Init a worker...")
        
        worker_instance = WorkerClass()
        
        run_logger.info("Init was succesfull! Running a worker...")
        
        await worker_instance.run()
      
    except KeyboardInterrupt as ke:
        run_logger.warning("Running was interrapted, end process...")
        sys.exit(0)
      
    except Exception as e:
        run_logger.critical(f"Something went wrong: {e}", exc_info=True)
        sys.exit(1)
    