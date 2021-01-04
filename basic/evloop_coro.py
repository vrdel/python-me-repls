#!/usr/bin/python3

import asyncio
import time
import inspect


async def coro1():
    await asyncio.sleep(5.0)
    print(f'coro1 - {time.ctime()}')
    return '123'


async def coro2():
    await asyncio.sleep(1.0)
    print(f'coro2 - {time.ctime()}')
    return '456'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        # serialized
        print(f'start {time.ctime()}')
        result = loop.run_until_complete(coro1())
        print(f'coro1 result {result}')
        result = loop.run_until_complete(coro2())
        print(f'coro2 result {result}')

        # concurrent
        result = loop.run_until_complete(asyncio.gather(coro1(), coro2()))
        print(f'coro1 + coro2 result {result}')
        print(f'end {time.ctime()}')

    finally:
        loop.close()
