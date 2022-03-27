import pathlib
from typing import Sequence

from trashcan.db import psycopg2_cur


REPORT_SQL_DIR = pathlib.Path(__file__).parent.absolute().joinpath('sql')


@psycopg2_cur()
def get_amenity_data_by_city(cursor, cities: Sequence[str], amenity: str):
    """
    Grab the count of amenity for a list of cities.
    """
    sql_file = REPORT_SQL_DIR.joinpath('amenity_counts_by_city.sql')

    with open(sql_file) as fp:
        sql_str = fp.read()
        params = {
            'amenity': amenity,
            'cities': cities
        }
        cursor.execute(sql_str, params)

    return cursor.fetchall()
