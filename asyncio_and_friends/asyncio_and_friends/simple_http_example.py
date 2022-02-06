"""
Usage:
    python simple_http_example.py [sync|async]

Description:
    Simple Python script to show the differences in implementation/speed of
    synchronous and asynchronous approach for downloading content.

    The output will show what was downloaded. The script repeats five
    times and prints the average run speed before exiting.
"""
import asyncio
import sys
import timeit

import aiohttp
import requests

# This URL holds open street map tiles.
# The range and zoom level grab tiles around Portland, OR, USA
TILE_SERVER_URL = 'https://tile-a.openstreetmap.fr/hot/13/1300/'
START = 2920
STOP = 2940


def main_sync():
    """
    Simple sync function that downloads files from our tile server
    """
    for id_ in range(START, STOP):
        url = f'{TILE_SERVER_URL}{id_}.png'
        print(url)
        resp = requests.get(url)
        print(resp.status_code)


async def main_async():
    """
    Simple async function that downloads 10 files from a CDN
    """

    async def _get(url):
        print(url)
        resp = await session.get(url)
        print(resp.status)

    async with aiohttp.ClientSession() as session:
        urls = tuple(f'{TILE_SERVER_URL}{id_}.png' for id_ in range(START, STOP))
        await asyncio.gather(*(_get(url) for url in urls))


funcs = {
    'sync': main_sync,
    'async': lambda: asyncio.run(main_async())
}


def main():
    script_type = None

    if len(sys.argv) > 1:
        script_type = sys.argv[1].lower()

    main_func = funcs.get(script_type)

    if main_func is None:
        sys.stderr.write('main function type not found\n')
        sys.exit(1)

    seconds = timeit.timeit(main_func, number=5)
    print(f'Avg over 5 attempts: {seconds / 5}')


if __name__ == '__main__':
    main()
