from pprint import pprint
import click

from trashcan.report.amenities import get_amenity_data_by_city


@click.group()
def report():
    """
    These sub-commands are responsible for generating reports
    """


@click.command('amenity_city')
@click.argument('cities', type=str)
@click.argument('amenity', type=str)
def amenity_count_by_city(cities, amenity):
    cities = tuple(cty.strip() for cty in cities.split(','))
    pprint(
        get_amenity_data_by_city(cities, amenity)
    )


report.add_command(amenity_count_by_city)
