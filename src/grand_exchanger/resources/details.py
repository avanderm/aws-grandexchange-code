"""Module for item details API resources."""
from dataclasses import dataclass

import desert
import marshmallow
import requests
import retrying

from .common import Item
from .helpers import retry_cases
from ..exceptions import NoSuchItemException


API_URL = (
    "https://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?"
    "item={item_id}"
)


ItemSchema = desert.schema_class(Item, meta={"unknown": marshmallow.EXCLUDE})()


@dataclass
class ItemDetails:
    """Representation for item details."""

    item: Item = desert.field(marshmallow_field=marshmallow.fields.Nested(ItemSchema))


schema = desert.schema(ItemDetails, meta={"unknown": marshmallow.EXCLUDE})


@retrying.retry(
    retry_on_exception=retry_cases, wait_random_min=1000, wait_random_max=3000
)
def get_item_details(item_id: int) -> ItemDetails:
    """Parses an item details payload.

    Args:
        item_id (int): A valid item ID.

    Returns:
        ItemDetails: An item details object.

    Raises:
        NoSuchItemException: An invalid item ID was provided.
    """
    try:
        with requests.get(API_URL.format(item_id=item_id)) as response:
            response.raise_for_status()
            return schema.load(response.json())
    except requests.HTTPError:
        raise NoSuchItemException
