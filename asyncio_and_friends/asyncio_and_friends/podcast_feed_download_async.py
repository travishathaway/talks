import asyncio
from typing import cast
from urllib import parse

import aiofiles
import aiohttp
import click
import feedparser


async def limited_download(urls: tuple[str], limit: int = 10, verbose: bool = False) -> None:
    """
    Downloads files asynchronously but limits concurrency to `limit`
    """
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(limit)  # This allows us a to limit our concurrency.

        async def _download_url(url):
            async with sem:
                if verbose:
                    print(url)
                await download_url(session, url)

        tasks = tuple(_download_url(url) for url in urls)
        await asyncio.gather(*tasks)


async def download_url(session: aiohttp.ClientSession, url: str) -> None:
    """Downloads single file using aiohttp.Session and saves file to disk"""
    file_name = parse.urlparse(url).path.split('/')[-1]

    async with aiofiles.open(file_name, 'wb') as fp:
        resp = await session.get(url)
        resp.raise_for_status()
        await fp.write(await resp.content.read())


def get_mp3_file_urls(feed: feedparser.FeedParserDict) -> tuple[str]:
    mp3_type = "audio/mpeg"

    return tuple(
        cast(str, link.href)
        for entry in feed.entries
        for link in entry.links
        if link.type == mp3_type
    )


@click.command()
@click.argument('podcast_feed_url')
@click.option('-l', '--limit', type=int)
@click.option('-b', '--batch-size', type=int, default=5)
@click.option('-v', '--verbose', is_flag=True)
def main(podcast_feed_url: str, limit: int, batch_size: int, verbose: bool) -> None:
    """
    Downloads files for a provided podcast feed URL. To limit total files downloaded,
    use the `limit` parameter. `batch_size` controls how many files are downloaded
    concurrently.
    """
    feed = feedparser.parse(podcast_feed_url)
    mp3_urls = get_mp3_file_urls(feed)[:limit]
    asyncio.run(limited_download(mp3_urls, limit=batch_size, verbose=verbose))


if __name__ == '__main__':
    main()
