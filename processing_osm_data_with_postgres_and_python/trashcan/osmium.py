import subprocess
from pathlib import Path

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
