#!/usr/bin/python3

import asyncio
import functools
import os
import signal
import time

def callback(n, loop):
    print(f'callback {n} invoked at {loop.time()}')

async def coro(loop):
    now = loop.time()
    print(f'clock time: {time.time()}')
    print(f'loop time: {now}')

    print('registering callback')
    loop.call_at(now + 2, callback, 1, loop)
    loop.call_at(now + 1, callback, 2, loop)
    loop.call_soon(callback, 3, loop)
    await asyncio.sleep(1)


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    try:
        print('entering event loop')
        event_loop.run_until_complete(coro(event_loop))
    finally:
        print('closing event loop')
        event_loop.close()


