import os
import json

import click
from trashcan.commands.data import data
from trashcan.config import parse_config_file


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = parse_config_file()


cli.add_command(data)


if __name__ == "__main__":
    cli()
