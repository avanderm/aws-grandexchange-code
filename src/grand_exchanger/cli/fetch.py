from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import sys


import click


from grand_exchanger import __version__, exceptions, models


@dataclass
class DateRange:
    start: datetime
    end: datetime

    def contains(self, dt: datetime) -> bool:
        if dt >= self.start and dt < self.end:
            return True
        else:
            return False


@click.group()
@click.version_option(version=__version__)
@click.option("--start", "-t0", type=click.DateTime(), help="Start date")
@click.option("--final", "-t1", type=click.DateTime(), help="End date")
@click.option("--date", "-t", type=click.DateTime(), help="Specific date")
@click.pass_context
def cli(ctx: click.Context, start: datetime, final: datetime, date: datetime) -> None:
    if (start or final) and date:
        click.secho(
            "Simultaneous intervals and specific dates are not supported.", fg="red"
        )
        sys.exit(1)

    if not date:
        ctx.obj = DateRange(
            start if start else datetime.now() - timedelta(days=1000),
            final if final else datetime.now(),
        )
    else:
        ctx.obj = DateRange(date, date + timedelta(days=1))


@cli.command("item")
@click.option("--id", "-i", type=int, required=True)
@click.pass_obj
def item(interval: DateRange, id: int) -> None:
    try:
        item = models.Item.get(id)
        category = models.Category.get_category_for_item(item)

        for dt, price in item.get_historical_prices():
            if interval.contains(dt):
                measurement = models.PriceMeasurement(item, category, price, dt)
                click.echo(json.dumps(measurement.to_dict()))

    except exceptions.NoSuchItemException:
        click.secho("Invalid item", fg="red")
        sys.exit(1)


@cli.command("category")
@click.option("--id", "-i", type=int, required=True)
@click.pass_obj
def category(interval: DateRange, id: int) -> None:
    try:
        category = models.Category.get(id)

        for item in category.get_items():
            for dt, price in item.get_historical_prices():
                if interval.contains(dt):
                    measurement = models.PriceMeasurement(item, category, price, dt)
                    click.echo(json.dumps(measurement.to_dict()))

    except exceptions.NoSuchCategoryException:
        click.secho("Invalid category", fg="red")
        sys.exit(1)
