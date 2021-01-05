#!/usr/bin/python3

import aiohttp
import asyncio


async def aiohttp_get():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(aiohttp_get())
    finally:
        loop.close()
