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
