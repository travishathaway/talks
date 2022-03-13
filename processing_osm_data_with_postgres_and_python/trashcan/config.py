import json
import sys
from dataclasses import dataclass
from functools import wraps
from typing import Sequence

import click


@dataclass
class CityConfig:
    name: str
    bundesland: str
    population: int
    osm_data_link: str
    bbox: list[float]


@dataclass
class Config:
    pgdsn: str = None
    cities: Sequence[CityConfig] = None


CONFIG = None


def parse_config_file():
    global CONFIG

    try:
        with open('./trash_config.json', 'r') as f:
            data = json.load(f)
            cities = tuple(
                CityConfig(**city)
                for city in data.get('cities', [])
            )
            CONFIG = Config(pgdsn=data.get('pgdsn', ''), cities=cities)
            return CONFIG

    except FileNotFoundError:
        click.echo(click.style(
            'Could not find config file. Please make sure it is named "trash_config.json"'
            'and present in the current directory', fg='red'
        ))
        sys.exit(1)
    except json.JSONDecodeError as exc:
        click.echo(click.style(
            f'Could not read JSON: {exc}', fg='red'
        ))
        sys.exit(1)


def get_config(f):
    """Parses and returns the current config object"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = CONFIG or parse_config_file()
        return f(config, *args, **kwargs)
    return wrapper
