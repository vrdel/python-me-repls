#!/usr/bin/python3

import aiohttp
import asyncio
import time
import ssl
import uvloop
import xml.dom.minidom


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


async def aiohttp_get(url, paginated=False):
    sslcontext = ssl.create_default_context(capath='/etc/grid-security/certificates/')
    sslcontext.load_cert_chain('hostcert.pem', 'hostkey.pem')

    suffix = url.split('method=')[1]

    print('aiohttp_get - started', f' - {time.ctime()}')
    try:
        async with aiohttp.ClientSession() as session:
            if paginated:
                count, cursor = 1, 0
                while count != 0:
                    async with session.get(url + f'&scope=&next_cursor={cursor}', ssl=sslcontext) as resp:
                        content = await resp.text()
                        parsed = xml.dom.minidom.parseString(content)
                        write_file(suffix, content)
                        count = int(parsed.getElementsByTagName('count')[0].childNodes[0].data)
                        links = parsed.getElementsByTagName('link')
                        for le in links:
                            if le.getAttribute('rel') == 'next':
                                href = le.getAttribute('href')
                                for e in href.split('&'):
                                    if 'next_cursor' in e:
                                        cursor = e.split('=')[1]
                print(f'file-{suffix} written', f' - {time.ctime()}')
            else:
                async with session.get(url, ssl=sslcontext) as resp:
                    print(f'HTTP {suffix} ', resp.status, f' - {time.ctime()}')
                    content = await resp.text()
                    write_file(suffix, content)
                    print(f'file-{suffix} written', f' - {time.ctime()}')

    except Exception as e:
        print(type(e))
        print(e)


async def sequential(paginated=False):
    await aiohttp_get(SITESPI, paginated)
    await aiohttp_get(SERVENDPI, paginated)
    await aiohttp_get(SERVGROUPPI, paginated)


if __name__ == '__main__':
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        print("Concurrent", f'- {time.ctime()}')
        loop.run_until_complete(asyncio.gather(
            aiohttp_get(SITESPI, paginated=True),
            aiohttp_get(SERVENDPI, paginated=True),
            aiohttp_get(SERVGROUPPI, paginated=True),
        ))
        print("End", f'- {time.ctime()}')
        print("Sequential", f'- {time.ctime()}')
        loop.run_until_complete(sequential())
        print("End", f'- {time.ctime()}')

    finally:
        loop.close()
