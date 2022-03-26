from functools import wraps

import psycopg2
from psycopg2.extras import NamedTupleCursor

from trashcan.config import get_config


@get_config
def psycopg2_cur(config):
    """Wrap function to setup and tear down a Postgres connection while
    providing a cursor object to make queries with.
    """
    def wrap(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Setup postgres connection
            connection = psycopg2.connect(config.pgdsn)

            try:
                cursor = connection.cursor(cursor_factory=NamedTupleCursor)
                # Call function passing in cursor
                return_val = f(cursor, *args, **kwargs)
            finally:
                # Close connection
                connection.commit()
                connection.close()

            return return_val

        return wrapper

    return wrap


@psycopg2_cur()
def get_amenity_count(cursor, amenity: str):
    sql = '''
    WITH all_amenity_count as (
        SELECT count(*) as cnt FROM amenity_polygons WHERE type = %(amenity)s
        UNION
        SELECT count(*) as cnt FROM amenity_points WHERE type = %(amenity)s
    )
    SELECT sum(cnt) FROM all_amenity_count
    '''
    cursor.execute(sql, {'amenity': amenity})
    res = cursor.fetchone()
    print(res)
