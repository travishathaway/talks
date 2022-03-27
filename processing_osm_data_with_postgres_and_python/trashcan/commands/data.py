import os
import tempfile
import pathlib
from contextlib import contextmanager
from functools import partial

import click


from trashcan.validators import validate_json_file
from trashcan import osm


@contextmanager
def osm_tempfile_manager():
    """
    Special context manager for temporary OSM data files we create during processing
    """
    fid, fname = tempfile.mkstemp(suffix='.osm.pbf')
    yield fid, fname
    os.remove(fname)


@click.group()
def data():
    """
    Sub command group for managing data within a trashcan project.
    """


@click.command('import')
@click.argument(
    'osm_file', type=click.Path(
        file_okay=True, dir_okay=False, readable=True, exists=True
    )
)
@click.option('-f', '--filters', type=str)
@click.option('-O', '--output', type=str)
@click.option('-S', '--style', type=str)
@click.option('-d', '--database', type=str)
@click.option('-U', '--username', type=str)
@click.option('-W', '--password', is_flag=True)
@click.option('-H', '--host', type=str)
@click.option('-P', '--port', type=str)
@click.option('--silent', is_flag=True)
@click.option('--dry-run', is_flag=True)
def import_data(osm_file, filters, output, style, database, username, password, host, port, silent, dry_run):
    """
    Import all the OSM db files for a project.
    Projects are defined via .json files.
    """
    with osm_tempfile_manager() as (fid, fname):
        try:
            osm.tags_filter(fname, osm_file, filters=filters, silent=silent, dry_run=dry_run)
            osm.osm2pgsql(
                fname, database=database,
                username=username, password=password,
                port=port, host=host,
                output=output, style=style, silent=silent, dry_run=dry_run
            )
        except Exception as exc:
            click.echo(
                f"{click.style('Exception raised during execution', fg='red')}"
                f" {exc}"
            )


@click.command('extract')
@click.argument('config', type=click.File(), callback=validate_json_file)
@click.argument('osm_data_file')
@click.option('-o', '--output', type=str, default='project-data.osm.pbf')
@click.option('--silent', is_flag=True)
@click.option('--dry-run', is_flag=True)
def extract(config, osm_data_file, output, silent, dry_run):
    """
    Extracts the given bounding boxes in CONFIG and combines them all into a single osm.pbf file
    """
    extracts = config.get('extracts', [])

    with tempfile.TemporaryDirectory() as tempdir:
        extracts = tuple(
            (pathlib.Path(tempdir).joinpath(ext['output']), ext) for ext in extracts
        )
        # Create extracts
        extract_func = partial(osm.extract, osm_data_file, dry_run=dry_run, silent=silent)
        tuple(map(lambda args: extract_func(*args), extracts))

        # Merge them all in to one file
        output_extracts = (filename for filename, *_ in extracts)
        osm.merge(output_extracts, output=output, dry_run=dry_run, silent=silent)


data.add_command(import_data)
data.add_command(extract)

