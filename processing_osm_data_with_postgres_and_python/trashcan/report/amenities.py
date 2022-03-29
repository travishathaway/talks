import pathlib
from typing import Sequence, Optional

import plotly.graph_objects as go

from trashcan.db import psycopg2_cur


REPORT_SQL_DIR = pathlib.Path(__file__).parent.absolute().joinpath('sql')


AMENITY_DATA_FIELDS = {
    'city': 'city',
    'amenity': 'amenity',
    'area_sq_km': 'area_sq_km',
    'count': 'count',
    'amenity_per_sq_km': 'amenity_per_sq_km',
}


@psycopg2_cur()
def get_amenity_data_by_city(cursor, cities: Sequence[str], amenity: str):
    """
    Grab the count of amenity for a list of cities.
    """
    sql_file = REPORT_SQL_DIR.joinpath('amenity_counts_by_city.sql')

    with open(sql_file) as fp:
        sql_str = fp.read()

    sql_str = sql_str.format(**AMENITY_DATA_FIELDS)
    params = {
        'amenity': amenity,
        'cities': cities
    }
    cursor.execute(sql_str, params)

    return cursor.fetchall()


def create_bar_chart(
        data: Sequence,
        x: str,
        y: str,
        output_file: str = 'chart.html',
        title: str = 'Bar Chart',
        xaxis_title: Optional[str] = None,
        yaxis_title: Optional[str] = None
) -> None:
    """
    Creates a bar chart and saves it to disk.
    """
    fig = go.Figure(go.Bar(
        x=[getattr(row, x) for row in data],
        y=[getattr(row, y) for row in data],
        orientation='h'
    ))
    xaxis_title = xaxis_title or x
    yaxis_title = yaxis_title or y

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(
            family="Lora",
            size=32,
            color="#666"
        ),
        xaxis=dict(
            color='#999'
        ),
        yaxis=dict(
            color='#666',
            tickfont=dict(
                size=36
            ),
            title=dict(
                font=dict(
                    color='#999'
                )
            )
        )
    )
    fig.show()
    # fig.write_html(output_file)
