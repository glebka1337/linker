# src/workers/linker/run.py
from src.workers.base_run import run_worker
import asyncio
from src.workers.linker.worker import LinkerWorker

async def main():
    await run_worker(LinkerWorker)

if __name__ == '__main__':
    asyncio.run(main())