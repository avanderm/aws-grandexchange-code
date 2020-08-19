"""Module for application specific exceptions."""


class NoSuchItemException(Exception):
    """Denotes a non-existent item."""

    pass


class NoSuchCategoryException(Exception):
    """Denotes a non-existent category."""

    pass
