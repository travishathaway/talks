import asyncio
import math
from typing import cast, Sequence, TypeVar
from urllib import parse

import aiofiles
import aiohttp
import click
import feedparser

T = TypeVar('T')


async def batch_download(links: tuple[str], batch_size: int = 10, verbose: bool = False) -> None:
    """
    Downloads files asynchronously in batches of `batch_size`
    """
    async with aiohttp.ClientSession() as session:
        batches = batch_items(links, batch_size)
        for idx, batch in enumerate(batches):
            if verbose:
                print(f"Downloading batch {idx + 1}")
            tasks = tuple(download_link(session, url, verbose=verbose) for url in batch)
            await asyncio.gather(*tasks)


async def download_link(session: aiohttp.ClientSession, url: str, verbose: bool = None) -> None:
    """Downloads single file using aiohttp.Session and saves file to disk"""
    file_name = parse.urlparse(url).path.split('/')[-1]
    if verbose:
        print(url)
    async with aiofiles.open(file_name, 'wb') as fp:
        resp = await session.get(url)
        await fp.write(await resp.content.read())


def batch_items(seq: Sequence[T], batch_size: int) -> tuple[Sequence[T]]:
    """
    This function is used to group items of a sequence. In this script,
    it's used to batch out the async tasks.
    """
    batches = math.ceil(len(seq) / batch_size)
    return tuple(
        seq[idx * batch_size: idx * batch_size + batch_size]
        for idx in range(batches)
    )


def get_mp3_file_links(feed: feedparser.FeedParserDict) -> tuple[str]:
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
    mp3_links = get_mp3_file_links(feed)[:limit]
    asyncio.run(batch_download(mp3_links, batch_size=batch_size, verbose=verbose))


if __name__ == '__main__':
    main()
