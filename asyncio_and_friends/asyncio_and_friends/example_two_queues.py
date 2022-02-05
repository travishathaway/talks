"""
This is a demonstration program which illustrates how to work with asyncio queues.
"""
import asyncio


async def save() -> None:
    """
    Worker task to save an entry to our SQLite database
    """


async def get():
    """
    Worker task for retrieving a set of records
    """


async def main() -> None:
    """
    Entry point for the script that queries a Rest API from <tbd>
    and inserts the records in a SQLite database.
    """
    queue = asyncio.Queue()


if __name__ == '__main__':
    asyncio.run(main())
