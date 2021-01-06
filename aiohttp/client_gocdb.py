#!/usr/bin/python3

import aiohttp
import asyncio
import time
import ssl


# paginated API
# SERVENDPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_endpoint&scope=&next_cursor=0'
# no paginated API
SERVENDPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_endpoint'

# no paginated API
# SITESPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_site&scope=&next_cursor=0'
SITESPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_site'

# no paginated API
# SERVGROUPPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_group&scope=&next_cursor=0'
SERVGROUPPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_group'


def write_file(suffix, content):
    with open(f'file-{suffix}', 'a') as fn:
        fn.write(content)
        fn.write("\n")


async def aiohttp_get(url):
    sslcontext = ssl.create_default_context(capath='/etc/grid-security/certificates/')
    sslcontext.load_cert_chain('hostcert.pem', 'hostkey.pem')

    suffix = url.split('method=')[1]

    print('aiohttp_get - started', f' - {time.ctime()}')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=sslcontext) as resp:
                print(f'HTTP {suffix} ', resp.status, f' - {time.ctime()}')
                content = await resp.text()
                write_file(suffix, content)
                print(f'file-{suffix} written', f' - {time.ctime()}')

    except Exception as e:
        print(type(e))
        print(e)


async def sequential():
    await aiohttp_get(SITESPI)
    await aiohttp_get(SERVENDPI)
    await aiohttp_get(SERVGROUPPI)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        print("Concurrent", f'- {time.ctime()}')
        loop.run_until_complete(asyncio.gather(
            aiohttp_get(SITESPI),
            aiohttp_get(SERVENDPI),
            aiohttp_get(SERVGROUPPI),
        ))
        print("End", f'- {time.ctime()}')
        print("Sequential", f'- {time.ctime()}')
        loop.run_until_complete(sequential())
        print("End", f'- {time.ctime()}')

    finally:
        loop.close()
