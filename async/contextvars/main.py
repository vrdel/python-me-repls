#!/usr/bin/python3

import asyncio
from example.context import request_id
from example.worker import worker

async def main():
    # request_id.set("START")

    await asyncio.gather(
        worker("task1"),
        worker("task2"),
    )

if __name__ == "__main__":
    asyncio.run(main())
