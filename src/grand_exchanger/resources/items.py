from dataclasses import dataclass
from typing import List

import desert
import marshmallow
import requests

from .helpers import Price

API_URL = (
    "https://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?"
    "category={category_id}&alpha={letter}&page={page}"
)


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


schema = desert.schema(Items, meta={"unknown": marshmallow.EXCLUDE})


def get_items_page(category_id: int, letter: str, page: int) -> Items:
    with requests.get(
        API_URL.format(category_id=category_id, letter=letter, page=page)
    ) as response:
        response.raise_for_status()
        return schema.load(response.json())
