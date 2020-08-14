from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Tuple

from grand_exchanger import resources


@dataclass
class Item:
    id: int
    name: str
    members: bool

    def get_historical_prices(self) -> Iterator[Tuple[datetime, int]]:
        yield from resources.get_historical_prices(self.id).list_daily_prices()
