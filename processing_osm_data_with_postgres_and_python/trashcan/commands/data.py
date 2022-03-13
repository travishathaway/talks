import click

from trashcan.validators import validate_json_file
from trashcan.osmium import extract


@click.group()
def data():
    """
    Sub command group for managing data within a trashcan project.
    """


@click.command('import')
@click.argument('osm_file', type=click.Path(file_okay=True, dir_okay=False, readable=True, exists=True))
@click.argument('config', type=click.File(), callback=validate_json_file)
def import_data(osm_file, config):
    """
    Import all the OSM db files for a project.
    Projects are defined via .json files.
    """
    cities = config.get('cities', [])
    extract(osm_file, cities[0])


data.add_command(import_data)
