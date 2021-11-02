#!/usr/bin/python3

import aiohttp
import aiohttp.client_exceptions
import asyncio
import time
import ssl
import uvloop
import xml.dom.minidom
from aiohttp_retry import RetryClient, ExponentialRetry, ListRetry

import logging
import logging.handlers

log = logging.getLogger('aiohttp_retry')
log.setLevel(logging.DEBUG)
log.addHandler(logging.handlers.SysLogHandler('/dev/log', logging.handlers.SysLogHandler.LOG_USER))
log.addHandler(logging.StreamHandler())

SERVENDPI = 'https://dp.eudat.eu/gocdbpi/gocdbpi/private/?method=get_service_endpoint'
SERVGROUPPI = 'https://dp.eudat.eu/gocdbpi/private/?method=get_service_group'


def write_file(suffix, content):
    with open(f'file-{suffix}', 'a') as fn:
        fn.write(content)
        fn.write("\n")


async def aiohttp_get(url):
    sslcontext = ssl.create_default_context(capath='/etc/grid-security/certificates/')
    sslcontext.load_cert_chain('hostcert.pem', 'hostkey.pem')

    auth = aiohttp.BasicAuth('xxxx', 'xxxx')

    suffix = url.split('method=')[1]

    http_retry_options = ExponentialRetry(attempts=2)
    client_timeout = aiohttp.ClientTimeout(total=1*15, connect=None,
                                           sock_connect=None, sock_read=None)
    conn_try, connection_attempts = 1, 3

    print('aiohttp_get - started', f' - {time.ctime()}')
    try:
        async with RetryClient(retry_options=http_retry_options, timeout=client_timeout) as session:
            async with session.get(url, ssl=sslcontext, auth=auth) as resp:
                print(f'HTTP {suffix} ', resp.status, f' - {time.ctime()}')
                content = await resp.text()
                write_file(suffix, content)
                print(f'file-{suffix} written', f' - {time.ctime()}')

    except Exception as e:
        print(type(e))
        print(e)


async def sequential():
    await aiohttp_get(SERVENDPI)
    await aiohttp_get(SERVGROUPPI)


if __name__ == '__main__':
    try:
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        print("Concurrent", f'- {time.ctime()}')
        loop.run_until_complete(asyncio.gather(
            aiohttp_get(SERVENDPI),
            aiohttp_get(SERVGROUPPI),
        ))
        print("End", f'- {time.ctime()}')
        print("Sequential", f'- {time.ctime()}')
        loop.run_until_complete(sequential())
        print("End", f'- {time.ctime()}')

    finally:
        loop.close()
