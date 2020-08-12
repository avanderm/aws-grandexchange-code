from dataclasses import dataclass
from typing import List


@dataclass
class LetterCount:
    letter: str
    items: int


@dataclass
class Category:
    alpha: List[LetterCount]
