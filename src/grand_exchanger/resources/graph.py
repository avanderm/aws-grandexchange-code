"""Module for item price graphs."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterator

import desert
import marshmallow
import requests
import retrying

from .helpers import Price, retry_cases, TimeStamp

API_URL = "https://services.runescape.com/m=itemdb_rs/api/graph/{item_id}.json"


@dataclass
class Graph:
    """Representation of an graph with prices for an item."""

    daily: Dict[datetime, int] = desert.field(
        marshmallow.fields.Dict(keys=TimeStamp, values=Price)
    )
    average: Dict[datetime, int] = desert.field(
        marshmallow.fields.Dict(keys=TimeStamp, values=Price)
    )

    def list_daily_prices(self, ascending: bool = False) -> Iterator:
        """Yield daily prices for an item sorted by time.

        Args:
            ascending (bool): Yield prices going up in time.

        Yields:
            Tuple[datetime, int]: The next daily price point.
        """
        for dt in sorted(self.daily.keys(), reverse=not ascending):
            yield dt, self.daily[dt]

    def list_average_prices(self, ascending: bool = False) -> Iterator:
        """Yield averaged daily prices for an item sorted by time.

        Args:
            ascending (bool): Yield prices going up in time.

        Yields:
            Tuple[datetime, int]: The next averaged daily price point.
        """
        for dt in sorted(self.average.keys(), reverse=not ascending):
            yield dt, self.average[dt]


schema = desert.schema(Graph, meta={"unknown": marshmallow.EXCLUDE})


@retrying.retry(
    retry_on_exception=retry_cases, wait_random_min=1000, wait_random_max=3000
)
def get_historical_prices(item_id: int) -> Graph:
    """Parses a graph with prices in time for an item.

    Args:
        item_id (int): A valid item ID.

    Returns:
        Graph: A graph object.
    """
    with requests.get(API_URL.format(item_id=item_id)) as response:
        response.raise_for_status()
        return schema.load(response.json())
