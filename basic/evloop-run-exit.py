#!/usr/bin/python3

import asyncio

async def f(delay):
    await asyncio.sleep(delay)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    t1 = loop.create_task(f(60))
    t2 = loop.create_task(f(60))
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
