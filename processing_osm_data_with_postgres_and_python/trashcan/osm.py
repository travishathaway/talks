from itertools import chain
import subprocess
from pathlib import Path

import click

from trashcan.types import OSMCityData


def extract(osm_file: Path, city_config: OSMCityData) -> None:
    """
    Given a `city_config` object, extract the contents of `osmfile` according to the `bbox` property.
    """
    bbox_strings = (str(coord) for coord in city_config['bbox'])
    bbox_str = ','.join(bbox_strings)
    output_file = f'{city_config["name"].lower().replace(" ", "_")}.osm.pbf'

    command = [
        'osmium',
        'extract',
        '--bbox',
        bbox_str,
        '--output',
        output_file,
        osm_file,
    ]
    subprocess.run(command)


def tags_filter(
        output_file: str,
        osm_data_file: str,
        filters: str = None,
        silent: bool = False,
        dry_run: bool = False
) -> None:
    """
    Provide a simplified Python wrapper over `osmium`
    """
    command = list(filter(None, [
        'osmium',
        'tags-filter',
        '--overwrite',
        '--output',
        output_file,
        osm_data_file,
        *filters.split()
    ]))

    if not silent:
        click.echo(f"{click.style('Running Command:', fg='green')} {' '.join(command)}")
    if not dry_run:
        subprocess.run(command)


def osm2pgsql(
        osm_data_file: str,
        silent: bool = False,
        dry_run: bool = False,
        password: bool = False,
        **cmd_options
) -> None:
    """
    Simplified wrapper around `osm2pgsql`.
    """
    options = tuple(cmd_options.keys())
    command = ['osm2pgsql']
    command += list(chain(*[
        (f'--{opt}', str(cmd_options.get(opt)))
        for opt in options
        if cmd_options.get(opt) is not None
    ]))
    if password:
        command.append('--password')
    command.append(osm_data_file)

    if not silent:
        click.echo(f"{click.style('Running Command:', fg='green')} {' '.join(command)}")
    if not dry_run:
        subprocess.run(command)
