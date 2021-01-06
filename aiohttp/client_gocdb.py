#!/usr/bin/python3

import aiohttp
import asyncio
import time
import ssl


SERVENDPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_endpoint&scope=&next_cursor=0'
SITESPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_site&scope=&next_cursor=0'
SERVGROUPPI = 'https://goc.egi.eu/gocdbpi/private/?method=get_service_group&scope=&next_cursor=0'


async def aiohttp_get(url):
    sslcontext = ssl.create_default_context(capath='/etc/grid-security/certificates/')
    sslcontext.load_cert_chain('hostcert.pem', 'hostkey.pem')

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=sslcontext) as resp:
            print('HTTP ', resp.status, f' - {time.ctime()}')
            content = await resp.text()
            return content


async def fetch_service_endpoints(url):
    try:
        response = await aiohttp_get(url)
        print(response)
    except Exception as e:
        print(type(e))


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(fetch_service_endpoints(SERVENDPI))

    finally:
        loop.close()
