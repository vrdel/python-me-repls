import asyncio
from .context import request_id
from .logger import log

async def worker(name: str):
    log(f"{name} started with request_id={request_id.get()}")
    await asyncio.sleep(0.1)
    if name == 'task1':
        request_id.set(f"CHANGED_1")
        log(f"{name} updated request_id: {request_id.get()}")
    if name == 'task2':
        log(f"{name} request_id={request_id.get()}")
