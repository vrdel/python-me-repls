#!/usr/bin/python3

import aiohttp
import asyncio
import time


url1 = 'http://httpbin.org/get'
url2 = 'https://api.randomuser.me'


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status, f'{time.ctime()}')
            print(await resp.text())


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            aiohttp_get(url1),
            aiohttp_get(url1),
            aiohttp_get(url2),
            aiohttp_get(url2)
        ))
    finally:
        loop.close()
