from dataclasses import dataclass
from typing import Dict, Iterator

import desert
from marshmallow import fields

from .helpers import Price, TimeStamp


@dataclass
class Graph:
    daily: Dict[str, int] = desert.field(fields.Dict(keys=TimeStamp, values=Price))
    average: Dict[str, int] = desert.field(fields.Dict(keys=TimeStamp, values=Price))

    def list_daily_prices(self, ascending: bool = False) -> Iterator:
        for dt in sorted(self.daily.keys(), reverse=not ascending):
            yield dt, self.daily[dt]

    def list_average_prices(self, ascending: bool = False) -> Iterator:
        for dt in sorted(self.average.keys(), reverse=not ascending):
            yield dt, self.average[dt]
