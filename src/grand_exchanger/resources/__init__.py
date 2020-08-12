import desert
import marshmallow

from .category import Category, LetterCount
from .graph import Graph
from .items import Items

CategorySchema = desert.schema(Category, meta={"unknown": marshmallow.EXCLUDE})
GraphSchema = desert.schema(Graph, meta={"unknown": marshmallow.EXCLUDE})
ItemsSchema = desert.schema(Items, meta={"unknown": marshmallow.EXCLUDE})

__all__ = [
    "Category",
    "CategorySchema",
    "Graph",
    "GraphSchema",
    "Items",
    "ItemsSchema",
    "LetterCount",
]
