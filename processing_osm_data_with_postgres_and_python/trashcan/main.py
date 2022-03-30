import click

from trashcan.commands.extract import extract
from trashcan.commands.import_data import import_data
from trashcan.commands.report import report
from trashcan.config import parse_config_file


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['config'] = parse_config_file()


cli.add_command(import_data)
cli.add_command(extract)
cli.add_command(report)


if __name__ == "__main__":
    cli()
