#!/usr/bin/python3

import aiohttp
import asyncio
import time


url_beer = 'https://random-data-api.com/api/beer/random_beer'
url_crypto = 'https://random-data-api.com/api/crypto_coin/random_crypto_coin'


def write_file(suffix, content):
    with open(f'file-{suffix}', 'a') as fn:
        fn.write(content)
        fn.write("\n")


async def delay(seconds):
    await asyncio.sleep(seconds)
    return True


async def aiohttp_get(url):
    epoch_seconds = time.time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print('HTTP ', resp.status, f' - {time.ctime()}')
            content = await resp.text()
            return content


async def wrap_one(url, suffix):
    print('wrap_one - started -', f'{time.ctime()}')
    await asyncio.sleep(1)
    data = await aiohttp_get(url)
    write_file(suffix, data)


async def wrap_two(url, suffix):
    print('wrap_two - started -', f'{time.ctime()}')
    await asyncio.sleep(2)
    data = await aiohttp_get(url)
    write_file(suffix, data)


async def wrap(suffix, urlo, urlt):
    await wrap_one(urlo, suffix)
    await wrap_two(urlt, suffix)


async def wrap_delay(urlt):
    print("Delay started - ", f'{time.ctime()}')
    flag = await delay(5.0)
    if flag:
        await aiohttp_get(urlt)
    # never got here
    else:
        print("Not scheduled")


async def task_from_coro(suffix, urlo, urlt):
    task = asyncio.ensure_future(wrap_two(urlt, suffix))
    await wrap_one(urlo, suffix)
    await task


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        # sequential
        loop.run_until_complete(wrap(time.time(), url_beer, url_crypto))

        # delayed
        loop.run_until_complete(wrap_delay(url_beer))

        # concurrent
        suffix = time.time()
        loop.run_until_complete(asyncio.gather(
            wrap_one(url_beer, suffix),
            wrap_two(url_crypto, suffix)
        ))

        # concurrent
        loop.run_until_complete(task_from_coro(time.time(), url_beer,
                                               url_crypto))

    finally:
        loop.close()
