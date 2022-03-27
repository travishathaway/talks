from itertools import chain
import subprocess
from pathlib import Path
from typing import Iterable

import click

from trashcan.types import OSMCityData


def extract(
        osm_file: Path,
        output: Path,
        city_config: OSMCityData,
        dry_run: bool = False,
        silent: bool = False
) -> None:
    """
    Given a `city_config` object, extract the contents of `osmfile` according to the `bbox` property.
    """
    buffer = 0.05
    x_min, y_min, x_max, y_max = city_config['bbox']
    bbox = x_min - buffer, y_min - buffer, x_max + buffer, y_max + buffer
    bbox_strings = (str(coord) for coord in bbox)
    bbox_str = ','.join(bbox_strings)

    command = [
        'osmium',
        'extract',
        '--overwrite',
        '--bbox',
        bbox_str,
        '--output',
        str(output),
        str(osm_file),
    ]

    if not silent:
        click.echo(f"{click.style('Running Command:', fg='green')} {' '.join(command)}")
    if not dry_run:
        subprocess.run(command)


def merge(
        osm_files: Iterable[Path],
        output='project-data.osm.pbf',
        silent: bool = False,
        dry_run: bool = False
) -> None:
    """
    Provides a thin wrapper around the `osmium merge` command
    """
    command = [
        'osmium',
        'merge'
    ] + [
        str(filename) for filename in osm_files
    ] + [
        '--overwrite',
        '--output',
        output
    ]

    if not silent:
        click.echo(f"{click.style('Running Command:', fg='green')} {' '.join(command)}")
    if not dry_run:
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
