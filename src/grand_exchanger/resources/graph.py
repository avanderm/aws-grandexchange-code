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
    daily: Dict[datetime, int] = desert.field(
        marshmallow.fields.Dict(keys=TimeStamp, values=Price)
    )
    average: Dict[datetime, int] = desert.field(
        marshmallow.fields.Dict(keys=TimeStamp, values=Price)
    )

    def list_daily_prices(self, ascending: bool = False) -> Iterator:
        for dt in sorted(self.daily.keys(), reverse=not ascending):
            yield dt, self.daily[dt]

    def list_average_prices(self, ascending: bool = False) -> Iterator:
        for dt in sorted(self.average.keys(), reverse=not ascending):
            yield dt, self.average[dt]


schema = desert.schema(Graph, meta={"unknown": marshmallow.EXCLUDE})


@retrying.retry(
    retry_on_exception=retry_cases, wait_random_min=1000, wait_random_max=3000
)
def get_historical_prices(item_id: int) -> Graph:
    with requests.get(API_URL.format(item_id=item_id)) as response:
        response.raise_for_status()
        return schema.load(response.json())
