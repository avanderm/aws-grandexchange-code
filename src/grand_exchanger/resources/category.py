from dataclasses import dataclass
from typing import Iterator, List, Tuple

import desert
import marshmallow
import requests
import requests_html


API_URL = (
    "https://services.runescape.com/m=itemdb_rs/api/category.json?"
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


def get_category_breakdown(category_id: int) -> CategoryBreakdown:
    with requests.get(API_URL.format(category_id=category_id)) as response:
        response.raise_for_status()
        return schema.load(response.json())


CATEGORY_URL = "https://secure.runescape.com/m=itemdb_rs/catalogue"


def get_categories() -> Iterator[Tuple[int, str]]:
    session = requests_html.HTMLSession()
    response = session.get(CATEGORY_URL)

    for i in response.html.find(".categories a"):
        name = i.text
        category_id = int(i.attrs["href"].split("=")[-1])

        yield category_id, name
