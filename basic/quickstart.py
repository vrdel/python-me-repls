#!/usr/bin/python3

import asyncio
import time


async def main():
    print(f'{time.ctime()} Hello')
    await asyncio.sleep(2.0)
    print(f'{time.ctime()} Goodbye')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
