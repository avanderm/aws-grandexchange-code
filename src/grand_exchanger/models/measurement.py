from dataclasses import dataclass
from datetime import datetime

from .category import Category
from .item import Item


@dataclass
class PriceMeasurement:
    item: Item
    category: Category
    price: int
    dt: datetime

    def to_dict(self) -> dict:
        return {
            "measurement": "price",
            "tags": {
                "category": self.category.name,
                "item_id": self.item.id,
                "members": self.item.members,
            },
            "time": self.dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {"value": self.price},
        }
