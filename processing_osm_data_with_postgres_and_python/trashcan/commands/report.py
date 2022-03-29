from pprint import pprint
import click

from trashcan.report.amenities import (
    get_amenity_data_by_city, create_bar_chart, AMENITY_DATA_FIELDS
)

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
    data = get_amenity_data_by_city(cities, amenity)
    pprint(data)
    create_bar_chart(
        data,
        x=AMENITY_DATA_FIELDS['amenity_per_sq_km'],
        y=AMENITY_DATA_FIELDS['city'],
        title=f'Amenity count by city: {amenity}',
        xaxis_title='Amenity per sq. km',
        yaxis_title='Top 10 German cities (by pop.)'
    )


report.add_command(amenity_count_by_city)
