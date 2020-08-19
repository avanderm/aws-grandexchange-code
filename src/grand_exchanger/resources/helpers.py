"""Module for helper functionality."""
from datetime import datetime
import json
import re
from typing import Any, Mapping, Optional

from marshmallow import fields, ValidationError
import requests
import six
import urllib3.exceptions


def retry_cases(exception: Exception) -> bool:
    """Exceptions eligible for request retries."""
    return (
        isinstance(exception, requests.ConnectionError)
        or isinstance(exception, json.JSONDecodeError)
        or isinstance(exception, urllib3.exceptions.MaxRetryError)
    )


class TimeStamp(fields.Field):
    """Deserializes an epoch timestamp."""

    def _deserialize(
        self,
        value: str,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ) -> datetime:
        """Deserializes an epoch timestamp to a datetime object."""
        try:
            return datetime.utcfromtimestamp(int(value) / 1000)
        except ValueError as error:
            raise ValidationError("Invalid epoch timestamp") from error


class Price(fields.Field):
    """Deserializes a Runescape formatted price."""

    def _deserialize(
        self,
        value: Any,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ) -> int:
        """Deserializes a price string to an integer."""
        try:
            if isinstance(value, six.integer_types):
                return value
            else:
                price = value.replace(" ", "")
                m = re.search("^((?:[-+])?\d+(?:\.\d+)?)([kmb])$", price)

                if m:
                    base = float(m.group(1))
                    modifier = {"k": 1000, "m": 1000000, "b": 1000000000}[m.group(2)]

                    return int(base * modifier)
                else:
                    return int(price.replace(",", ""))
        except ValueError as error:
            raise ValidationError("Invalid price format") from error
