from dataclasses import dataclass
from typing import List

import desert
import marshmallow

from .helpers import Price


@dataclass
class PriceTrend:
    trend: str
    price: int = desert.field(Price())


@dataclass
class Item:
    id: int
    name: str
    description: str
    current: PriceTrend
    today: PriceTrend
    members: bool


ItemSchema = desert.schema_class(Item, meta={"unknown": marshmallow.EXCLUDE})()


@dataclass
class Items:
    total: int
    items: List[Item] = desert.field(
        marshmallow_field=marshmallow.fields.List(marshmallow.fields.Nested(ItemSchema))
    )
