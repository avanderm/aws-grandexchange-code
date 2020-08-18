from dataclasses import dataclass
from typing import Iterator, List, Tuple

import desert
import marshmallow
import requests
import requests_html
import retrying

from .helpers import retry_cases


API_URL = (
    "https://services.runescape.com/m=itemdb_rs/api/catalogue/category.json?"
    "category={category_id}"
)


@dataclass
class LetterCount:
    letter: str
    items: int


@dataclass
class CategoryBreakdown:
    alpha: List[LetterCount]


schema = desert.schema(CategoryBreakdown, meta={"unknown": marshmallow.EXCLUDE})


@retrying.retry(
    retry_on_exception=retry_cases, wait_random_min=1000, wait_random_max=3000
)
def get_category_breakdown(category_id: int) -> CategoryBreakdown:
    with requests.get(API_URL.format(category_id=category_id)) as response:
        response.raise_for_status()
        return schema.load(response.json())


CATEGORY_URL = "https://secure.runescape.com/m=itemdb_rs/catalogue"


@retrying.retry(
    retry_on_exception=retry_cases, wait_random_min=1000, wait_random_max=3000
)
def get_categories() -> Iterator[Tuple[int, str]]:
    session = requests_html.HTMLSession()
    response = session.get(CATEGORY_URL)

    categories = {}

    for i in response.html.find(".categories a"):
        name = i.text
        category_id = int(i.attrs["href"].split("=")[-1])

        categories[category_id] = name

    for i in sorted(categories):
        yield i, categories[i]
