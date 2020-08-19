"""Module for the info command group."""
from datetime import datetime
import json
import sys


import click


from grand_exchanger import __version__, exceptions, models


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """CLI group."""
    pass


@cli.command("item")
@click.argument("id", type=int, required=True)
def item(id: int) -> None:
    """Outputs a measurement for latest item price.

    Args:
        id (int): A valid item ID.
    """
    try:
        item = models.Item.get(id)
        category = models.Category.get_category_for_item(item)
        measurement = models.PriceMeasurement(
            item, category, item.price, datetime.now()
        )

        click.echo(json.dumps(measurement.to_dict()))
    except exceptions.NoSuchItemException:
        click.secho("Invalid item", fg="red")
        sys.exit(1)


@cli.command("category")
@click.argument("id", type=int, required=True)
def category(id: int) -> None:
    """Outputs measurements for latest item prices in a category.

    Args:
        id (int): A valid category ID.
    """
    try:
        category = models.Category.get(id)

        for item in category.get_items():
            measurement = models.PriceMeasurement(
                item, category, item.price, datetime.now()
            )
            click.echo(json.dumps(measurement.to_dict()))
    except exceptions.NoSuchCategoryException:
        click.secho("Invalid category", fg="red")
        sys.exit(1)


@cli.command("all")
def all() -> None:
    """Output price measurements for all items in the date range."""
    try:
        for category in models.Category.get_categories():
            for item in category.get_items():
                measurement = models.PriceMeasurement(
                    item, category, item.price, datetime.now()
                )
                click.echo(json.dumps(measurement.to_dict()))

    except exceptions.NoSuchCategoryException:
        click.secho("Invalid category", fg="red")
        sys.exit(1)
