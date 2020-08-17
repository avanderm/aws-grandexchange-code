from dataclasses import dataclass
from typing import Iterator, Tuple

from grand_exchanger import resources
from .item import Item


@dataclass
class Category:
    id: int
    name: str

    def get_items(self) -> Iterator[Item]:
        for i in self.get_item_current_prices():
            yield i[0]

    def get_item_current_prices(self) -> Iterator[Tuple[Item, int]]:
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
                        item = Item(i.id, i.name, i.members)
                        yield item, i.today.price

                        count += 1
                else:
                    empty_page = True

                page += 1
