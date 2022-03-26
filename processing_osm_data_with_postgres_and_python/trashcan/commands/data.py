import os
import tempfile
from contextlib import contextmanager

import click

from trashcan.osm import tags_filter, osm2pgsql


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
            tags_filter(fname, osm_file, filters=filters, silent=silent, dry_run=dry_run)
            osm2pgsql(
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


data.add_command(import_data)
