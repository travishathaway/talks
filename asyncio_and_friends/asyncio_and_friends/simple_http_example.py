"""
Usage:
    simple_http [OPTIONS] FUNC_TYPE

Options:
    --verbose|-v  Show more verbose output (shows which endpoints are being queried)

Description:
    Simple Python script to show the differences in implementation/speed of
    synchronous and asynchronous approach for downloading content.

    You specify the function to be run with the FUNC_TYPE argument (can either
    be 'sync' or 'async').
"""
import asyncio
import sys
import timeit
from typing import Callable

import aiohttp
import requests

# This URL holds open street map tiles.
# The range and zoom level grab tiles around Portland, OR, USA
TILE_SERVER_URL = 'https://tile-a.openstreetmap.fr/hot/13/1300/'
START = 2920
STOP = 2940


def main_sync(verbose=False):
    """
    Simple sync function that downloads files from our tile server
    """
    for id_ in range(START, STOP):
        url = f'{TILE_SERVER_URL}{id_}.png'
        if verbose:
            print(f'GET: {url}')
        resp = requests.get(url)
        # Normally, do something else with response...


async def main_async(verbose=False):
    """
    Simple async function that downloads 10 files from a CDN
    """

    async def _get(url):
        if verbose:
            print(f'GET: {url}')
        resp = await session.get(url)
        # Normally, do something else with response...

    async with aiohttp.ClientSession() as session:
        urls = tuple(f'{TILE_SERVER_URL}{id_}.png' for id_ in range(START, STOP))
        await asyncio.gather(*(_get(url) for url in urls))


funcs = {
    'sync': main_sync,
    'async': lambda verbose: asyncio.run(main_async(verbose))
}

Args = tuple[bool, Callable]


def parse_args() -> Args:
    """
    Inspects sys.argv to give us the two CLI args we care about (verbose and func_type).
    We try to find the appropriate function base on the value of func_type otherwise
    we exit the script.
    """
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    script_type = None

    if len(sys.argv) > 1:
        script_type = sys.argv[1].lower()

    main_func = funcs.get(script_type)

    if main_func is None:
        sys.stderr.write('Argument one must be either "sync" or "async"\n')
        sys.exit(1)

    return verbose, main_func


def main() -> None:
    verbose, main_func = parse_args()

    # Wrap main function call in another function (this makes it easier to use with `timeit.timeit`)
    def call_main_func():
        main_func(verbose)

    seconds = timeit.timeit(call_main_func, number=5)
    print(f'Avg over 5 attempts: {seconds / 5}')


if __name__ == '__main__':
    main()
