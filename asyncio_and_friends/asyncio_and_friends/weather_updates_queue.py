"""
This is a demonstration program which illustrates how to work with asyncio queues.

For it to work, you need to sign up for an open weather map account here:

    https://openweathermap.org

Once you've done that, set the environment variable OPEN_WEATHER_API_KEY
(this will be you API key from openweathermap.org)
"""
import asyncio
import os
import sys
from typing import NamedTuple

import aiohttp

API_KEY = os.getenv('OPEN_WEATHER_API_KEY')


class Point(NamedTuple):
    lat: float
    lon: float
    label: str


class CurrentWeatherInfo(NamedTuple):
    description: str
    temperature: int
    point: Point


async def get_weather_data(session: aiohttp.ClientSession, point: Point) -> CurrentWeatherInfo:
    """
    Get weather data for `point` from openweathermap.org
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={point.lat}&lon={point.lon}&appid={API_KEY}'

    resp = await session.get(url)
    data = await resp.json()

    description = ','.join(desc.get('description', 'n/a') for desc in data.get('weather', []))
    temperature = round(data.get('main', {}).get('temp', 0) - 273.15)

    return CurrentWeatherInfo(description=description, temperature=temperature, point=point)


async def main_async() -> None:
    points = (
        Point(lat=54.305902, lon=10.123282, label='Kiel'),
        Point(lat=52.521021, lon=13.381268, label='Berlin'),
        Point(lat=48.144049, lon=11.575928, label='München'),
    )

    queue = asyncio.Queue()

    async def produce(point: Point) -> None:
        while True:
            async with aiohttp.ClientSession() as session:
                weather_data = await get_weather_data(session, point)
                await queue.put(weather_data)
            await asyncio.sleep(5)

    async def consume() -> None:
        while True:
            data = await queue.get()
            print(f'{data.point.label}: {data.temperature} :: {data.description}')
            queue.task_done()

    asyncio.create_task(consume())

    await asyncio.gather(*(produce(point) for point in points))


def main():
    if API_KEY is None:
        print('Set the environment variable `OPEN_WEATHER_API_KEY`. '
              'Sign up for an account here: https://openweathermap.org')
        sys.exit(1)
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
