#!/usr/bin/python3

import asyncio
import time
import concurrent.futures
from functools import partial


def blocking(n, what, sleep):
    print(f"{time.ctime()} Started {what} {n} - Sleeping for {sleep} seconds")
    time.sleep(sleep)
    print(f"{time.ctime()} Ended {what} {n}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=5)
        blocking_tasks = [
            loop.run_in_executor(executor, partial(blocking, n, 'Task', 5.0))
            for n in range(5)]
        loop.run_until_complete(asyncio.gather(*blocking_tasks))
        print('All ended')

    finally:
        loop.close()
