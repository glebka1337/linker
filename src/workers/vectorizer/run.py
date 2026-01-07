# src/workers/vectorizer/run.py
from src.workers.base_run import run_worker
import asyncio
from src.workers.vectorizer.worker import VectorWorker

async def main():
    await run_worker(VectorWorker)

if __name__ == '__main__':
    asyncio.run(main())