# src/workers/base_run.py
import sys
import logging
from typing import TypeVar, Type
from src.core.logger import setup_logging
from src.core.resources import Resources
from src.workers.base import BaseWorker
from src.db.qdrant import (
    qdrant_client_manager,
    create_qdrant_collection
)
from src.db.mongo import mongo_beanie_manager
from src.db.rabbit import rabbitmq_conn_manager

WorkerType = TypeVar("WorkerType", bound=BaseWorker)

async def run_worker(
    WorkerClass: Type[BaseWorker]
):
    setup_logging()
    
    async with (
        qdrant_client_manager() as qdrant_client,
        mongo_beanie_manager() as mongo_client,
        rabbitmq_conn_manager() as rabbitmq_conn,
        
    ):
        resources = Resources(
            qdrant_client=qdrant_client,
            mongo_client=mongo_client,
            rabbitmq_conn=rabbitmq_conn
        )
        
        cls_name = WorkerClass.__name__
        run_logger = logging.getLogger(f"Runner: {cls_name}")
        
        try:
            run_logger.info("Init a worker...")
            
            worker_instance = WorkerClass()
            
            run_logger.info("Init was succesfull! Running a worker...")
            
            await worker_instance.run(
                resources
            )
        
        except KeyboardInterrupt as ke:
            run_logger.warning("Running was interrapted, end process...")
            sys.exit(0)
        
        except Exception as e:
            run_logger.critical(f"Something went wrong: {e}", exc_info=True)
            sys.exit(1)
        