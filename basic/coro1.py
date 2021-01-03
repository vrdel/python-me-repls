#!/usr/bin/python3

import asyncio
import time
import inspect


async def coro1():
    return '123'


if __name__ == '__main__':
    try:
        coro = coro1()

        print(type(coro))
        print(type(coro1))
        print(inspect.iscoroutine(coro))

        coro.send(None)

    except StopIteration as e:
        print('The answer is {}'.format(e.value))
        print(type(e))
