"""Module for common functionality."""
from dataclasses import dataclass

import desert

from .helpers import Price


@dataclass
class PriceTrend:
    """Representation of a price trend."""

    trend: str
    price: int = desert.field(Price())


@dataclass
class Item:
    """Representation of an item."""

    id: int
    name: str
    description: str
    type: str
    current: PriceTrend
    today: PriceTrend
    members: bool
