#!/usr/bin/python3

import asyncio
import time


async def coro1():
    print(f'{time.ctime()} Hello')
    await asyncio.sleep(10)
    print(f'{time.ctime()} Goodbye')


def blocking():
    time.sleep(5.0)
    print(f"{time.ctime()} Hello from a thread")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_in_executor(None, blocking)
        loop.run_until_complete(coro1())
    finally:
        loop.close()
