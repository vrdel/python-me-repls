#!/usr/bin/python3

import asyncio
import time
import concurrent.futures


def blocking(n):
    print(f"{time.ctime()} Started {n}")
    time.sleep(5.0)
    print(f"{time.ctime()} Ended {n}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    try:
        executor = concurrent.futures.ProcessPoolExecutor(max_workers=5)
        blocking_tasks = [
            loop.run_in_executor(executor, blocking, n)
            for n in range(5)]
        loop.run_until_complete(asyncio.gather(*blocking_tasks))
        print('All ended')

    finally:
        loop.close()
