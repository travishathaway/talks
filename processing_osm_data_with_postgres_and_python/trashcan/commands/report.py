import click

from trashcan.reports.amenities import (
    get_amenity_data_by_city,
    get_parking_area_by_city,
    AMENITY_DATA_FIELDS,
    PARKING_DATA_FIELDS,
)
from trashcan.charts import create_bar_chart, print_table

OUTPUT_TERMINAL = 'terminal'
OUTPUT_CHART = 'chart'


@click.group()
def report():
    """
    These sub-commands are responsible for generating reports
    """


@click.command('amenity_city')
@click.argument('cities', type=str)
@click.argument('amenity', type=str)
@click.option('-o', '--output', default=OUTPUT_TERMINAL)
def amenity_count_by_city(cities, amenity, output):
    cities = tuple(cty.strip() for cty in cities.split(','))
    data = get_amenity_data_by_city(cities, amenity)

    if output == OUTPUT_TERMINAL:
        print_table(data, title=f'Amenity county by city: {amenity}', fields=AMENITY_DATA_FIELDS)
    elif output == OUTPUT_CHART:
        create_bar_chart(
            data,
            x=AMENITY_DATA_FIELDS['amenity_per_sq_km']['name'],
            y=AMENITY_DATA_FIELDS['city']['name'],
            title=f'Amenity count by city: {amenity}',
            xaxis_title='Amenity per sq. km',
            yaxis_title='Top 10 German cities (by pop.)'
        )


@click.command('parking_space')
@click.argument('cities', type=str)
@click.option('-o', '--output', default=OUTPUT_TERMINAL)
def parking_space_by_city(cities, output):
    cities = tuple(cty.strip() for cty in cities.split(','))
    data = get_parking_area_by_city(cities)

    if output == OUTPUT_TERMINAL:
        print_table(data, title='Parking Area', fields=PARKING_DATA_FIELDS)
    elif output == OUTPUT_CHART:
        create_bar_chart(
            data,
            x=PARKING_DATA_FIELDS['percentage_parking_area']['name'],
            y=PARKING_DATA_FIELDS['city']['name'],
            title=f'Percentage parking area by city',
            xaxis_title='Percentage Parking area',
            yaxis_title='Top 10 German cities (by pop.)'
        )


report.add_command(amenity_count_by_city)
report.add_command(parking_space_by_city)
