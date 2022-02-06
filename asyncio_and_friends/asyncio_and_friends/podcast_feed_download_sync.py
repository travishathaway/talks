from typing import cast, Sequence
from urllib import parse

import click
import feedparser
import requests


def download_urls(urls: Sequence, verbose: bool = False) -> None:
    """
    Download and save all links in the `links` list
    """
    for url in urls:
        file_name = parse.urlparse(url).path.split('/')[-1]
        if verbose:
            print(f'Downloading: {file_name}')
        resp = requests.get(url)
        resp.raise_for_status()
        with open(file_name, 'wb') as fp:
            fp.write(resp.content)


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
@click.option('-v', '--verbose', is_flag=True)
def main(podcast_feed_url: str, limit: int, verbose: bool) -> None:
    """
    Synchronously download files from a podcast feed.
    """
    feed = feedparser.parse(podcast_feed_url)
    mp3_urls = get_mp3_file_urls(feed)[:limit]
    download_urls(mp3_urls, verbose=verbose)


if __name__ == '__main__':
    main()
