#!/usr/bin/python3

import asyncio
import time
import inspect


async def coro1():
    return '123'


async def coro2():
    # try remove
    await asyncio.sleep(1.0)
    return '456'


async def coro2_call():
    print("coro2_called")
    await asyncio.sleep(1.0)
    result = await coro2()
    print('The answer 3 is {}'.format(result))
    return result


if __name__ == '__main__':
    try:
        coro = coro1()

        print(type(coro))
        print(type(coro1))
        print(inspect.iscoroutine(coro))

        coro.send(None)

    except StopIteration as e:
        print('The answer 1 is {}'.format(e.value))
        print(type(e))

    try:
        coro = coro2()
        coro.send(None)

    except StopIteration as e:
        # never see this one. it can be seen only if asyncio.sleep() is removed
        # in coro2()
        print('The answer 2 is {}'.format(e.value))
        print(type(e))

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro2_call())
    finally:
        loop.close()
