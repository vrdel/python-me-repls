#!/usr/bin/python3

import asyncio
import functools
import os
import signal

async def f(delay):
    await asyncio.sleep(delay)

def signal_handler(name):
    print(f'signal_handler({name})')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(f(60))
    t2 = loop.create_task(f(60))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(signal_handler, name='SIGTERM'),)
    try:
        loop.run_until_complete(asyncio.gather(
            t1, t2
        ))
    except KeyboardInterrupt:
        print('Got signal: SIGINT, shutting down.')
    tasks = asyncio.Task.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
