import click
import json


def validate_json_file(_, __, value):
    """
    Ensures we have a valid JSON file before continuing.
    """
    try:
        return json.load(value)
    except json.JSONDecodeError as exc:
        raise click.BadArgumentUsage(f'Error decoding JSON: {exc}')
