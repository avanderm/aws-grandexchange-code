from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from grand_exchanger import resources
from .item import Item
from ..exceptions import NoSuchCategoryException


@dataclass
class Category:
    id: int
    name: str

    @property
    def total(self) -> int:
        breakdown = resources.get_category_breakdown(self.id)
        return sum(map(lambda x: x.items, breakdown.alpha))

    def get_items(self) -> Iterator[Item]:
        breakdown = resources.get_category_breakdown(self.id)

        for lc in breakdown.alpha:
            count = 0
            page = 1
            empty_page = False

            letter = lc.letter if lc.letter != "#" else "%23"

            while count < lc.items and not empty_page:
                batch = resources.get_items_page(self.id, letter, page)

                if batch.items:
                    for i in batch.items:
                        item = Item(i.id, i.name, self.name, i.members, i.current.price)
                        yield item

                        count += 1
                else:
                    empty_page = True

                page += 1

    @classmethod
    def get_categories(cls) -> Iterator[Category]:
        for category_id, name in resources.get_categories():
            yield cls(category_id, name)

    @classmethod
    def get(cls, category_id: int) -> Category:
        for c in cls.get_categories():
            if c.id == category_id:
                return c

        raise NoSuchCategoryException

    @classmethod
    def get_category_for_item(cls, item: Item) -> Category:
        for c in cls.get_categories():
            if c.name == item.type:
                return c

        raise NoSuchCategoryException
