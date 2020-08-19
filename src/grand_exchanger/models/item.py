"""Module for item classes."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Tuple

from grand_exchanger import resources


@dataclass
class Item:
    """Representation of an item."""

    id: int
    name: str
    type: str
    members: bool
    price: int

    def get_historical_prices(self) -> Iterator[Tuple[datetime, int]]:
        """Returns historical daily prices for this item.

        Yields:
            Tuple[datetime, int]: The next price point with corresponding timestamp.
        """
        yield from resources.get_historical_prices(self.id).list_daily_prices()

    @classmethod
    def get(cls, item_id: int) -> Item:
        """Returns an item object for an item ID.

        Args:
            item_id: A valid item ID.

        Returns:
            Item
        """
        details = resources.get_item_details(item_id)
        item = details.item

        return cls(item.id, item.name, item.type, item.members, item.current.price)

    def to_str(self) -> str:
        """Returns textual information for display.

        Returns:
            str: Multiline string summarizing the item.
        """
        return f"""
        {self.name} ({self.id}):
        category: {self.type}
        members: {self.members}

        price: {self.price}
        """
