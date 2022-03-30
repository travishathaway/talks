import tempfile
import pathlib
from functools import partial

import click

from osmprj.validators import validate_json_file
from osmprj import osm


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
