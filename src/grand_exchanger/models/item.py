from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Tuple

from grand_exchanger import resources


@dataclass
class Item:
    id: int
    name: str
    type: str
    members: bool
    price: int

    def get_historical_prices(self) -> Iterator[Tuple[datetime, int]]:
        yield from resources.get_historical_prices(self.id).list_daily_prices()

    @classmethod
    def get(cls, item_id: int) -> Item:
        details = resources.get_item_details(item_id)
        item = details.item

        return cls(item.id, item.name, item.type, item.members, item.current.price)

    def to_str(self) -> str:
        return f"""
        {self.name} ({self.id}):
        category: {self.type}
        members: {self.members}

        price: {self.price}
        """
