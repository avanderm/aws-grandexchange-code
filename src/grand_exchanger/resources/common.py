from dataclasses import dataclass

import desert

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
    type: str
    current: PriceTrend
    today: PriceTrend
    members: bool
