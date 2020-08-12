from datetime import datetime
import re
from typing import Any, Mapping, Optional

from marshmallow import fields, ValidationError
import six


class TimeStamp(fields.Field):
    """Deserializes an epoch timestamp.
    """

    def _deserialize(
        self,
        value: str,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ) -> datetime:
        try:
            return datetime.utcfromtimestamp(int(value) / 1000)
        except ValueError as error:
            raise ValidationError("Invalid epoch timestamp") from error


class Price(fields.Field):
    """Deserializes a Runescape formatted price.
    """

    def _deserialize(
        self,
        value: Any,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ) -> int:
        try:
            if isinstance(value, six.integer_types):
                return value
            else:
                price = value.strip()
                m = re.search("^(\d+(?:\.\d+)?)([kmb])$", price)

                if m:
                    base = float(m.group(1))
                    modifier = {"k": 1000, "m": 1000000, "b": 1000000000}[m.group(2)]

                    return int(base * modifier)
                else:
                    return int(price.replace(",", ""))
        except ValueError as error:
            raise ValidationError("Invalid price format") from error
