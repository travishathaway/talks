import click
from trashcan.commands.data import data


@click.group()
def cli():
    pass


cli.add_command(data)


if __name__ == "__main__":
    cli()
