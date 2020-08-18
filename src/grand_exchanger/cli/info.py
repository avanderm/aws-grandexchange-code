import sys

import click

from grand_exchanger import __version__, exceptions, models


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command("ls")
def list_categories() -> None:
    for c in models.Category.get_categories():
        click.secho(f"{c.id}: {c.name} ({c.total})", fg="green")


@cli.command("item")
@click.option("--id", "-i", type=int, required=True)
def item(id: int) -> None:
    try:
        obj = models.Item.get(id)
        click.secho(obj.to_str(), fg="green")
    except exceptions.NoSuchItemException:
        click.secho("Invalid item", fg="red")
        sys.exit(1)


@cli.command("category")
@click.option("--id", "-i", type=int, required=True)
def category(id: int) -> None:
    try:
        obj = models.Category.get(id)
        for i in obj.get_items():
            click.secho(i.to_str(), fg="green")
    except exceptions.NoSuchCategoryException:
        click.secho("Invalid category", fg="red")
        sys.exit(1)
