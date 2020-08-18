from datetime import datetime
import json
import sys


import click


from grand_exchanger import __version__, exceptions, models


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    pass


@cli.command("item")
@click.option("--id", "-i", type=int, required=True)
def item(id: int) -> None:
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
@click.option("--id", "-i", type=int, required=True)
def category(id: int) -> None:
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
