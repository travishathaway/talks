# Asnycio and Friends

To see the slides from this talk, [check them out on Google Docs](https://docs.google.com/presentation/d/1ate_nmSvK4C0jSuhrf7Jy1WB9IZQU3LmK6ao34Fzxjo/edit?usp=sharing)

## Setup

In order run the scripts contatined here, install this project via `poetry` (https://python-poetry.org/docs/):

```bash
$ poetry install
```

And then run a shell with:
```bash
$ poetry shell
```

## Available commands:

- `podcast_dl_async` "asyncio_and_friends.podcast_feed_download_async:main"
- `podcast_dl_sync`  "asyncio_and_friends.podcast_feed_download_sync:main"
- `simple_http`      "asyncio_and_friends.simple_http_example:main"
- `weather_example`  "asyncio_and_friends.weather_updates_queue:main"

For more details about the commands and what they do, I highly suggest reading through the source code.
