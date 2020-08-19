"""Tests for the resources package."""
from datetime import datetime

import marshmallow
import pytest
import requests

from grand_exchanger import exceptions, resources


class TestGraph:
    """Test class for grand_exchanger.resources.graph."""

    @pytest.fixture
    def mock_requests_get(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "daily": {"1595808000000": 100, "1595721600000": 120, "1595635200000": 110},
            "average": {
                "1595808000000": 100,
                "1595721600000": 110,
                "1595635200000": 104,
            },
        }

    @pytest.fixture
    def mock_requests_get_invalid(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "daily": {"not_an_epoch": 100, "1595721600000": 120, "1595635200000": 110},
            "average": {
                "1595808000000": 100,
                "1595721600000": 110,
                "1595635200000": 104,
            },
        }

    def test_get_historical_prices(self, mock_requests_get):
        """Epoch timestamps and prices are correctly converted."""
        from grand_exchanger.resources.graph import Graph

        result = resources.get_historical_prices(1)

        assert result == Graph(
            daily={
                datetime(2020, 7, 27, 0, 0): 100,
                datetime(2020, 7, 26, 0, 0): 120,
                datetime(2020, 7, 25, 0, 0): 110,
            },
            average={
                datetime(2020, 7, 27, 0, 0): 100,
                datetime(2020, 7, 26, 0, 0): 110,
                datetime(2020, 7, 25, 0, 0): 104,
            },
        )

    def test_get_historical_prices_bad_timestamp(self, mock_requests_get_invalid):
        """Non epoch timestamps cause an error."""
        with pytest.raises(marshmallow.ValidationError):
            resources.get_historical_prices(1)

    def test_list_daily_prices(self):
        """Daily prices are correctly returned."""
        from grand_exchanger.resources.graph import Graph

        price_history = Graph(
            daily={
                datetime(2020, 7, 26, 0, 0): 120,
                datetime(2020, 7, 25, 0, 0): 110,
                datetime(2020, 7, 27, 0, 0): 100,
            },
            average={},
        )

        assert list(price_history.list_daily_prices()) == [
            (datetime(2020, 7, 27, 0, 0), 100),
            (datetime(2020, 7, 26, 0, 0), 120),
            (datetime(2020, 7, 25, 0, 0), 110),
        ]

    def test_list_average_prices(self):
        """Daily average prices are correctly returned."""
        from grand_exchanger.resources.graph import Graph

        price_history = Graph(
            daily={},
            average={
                datetime(2020, 7, 26, 0, 0): 100,
                datetime(2020, 7, 27, 0, 0): 104,
                datetime(2020, 7, 25, 0, 0): 110,
            },
        )

        assert list(price_history.list_average_prices()) == [
            (datetime(2020, 7, 27, 0, 0), 104),
            (datetime(2020, 7, 26, 0, 0), 100),
            (datetime(2020, 7, 25, 0, 0), 110),
        ]


class TestCategoryBreakdown:
    """Test class for grand_exchanger.resources.category."""

    @pytest.fixture
    def mock_requests_get(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "types": [],
            "alpha": [
                {"letter": "#", "items": 0},
                {"letter": "a", "items": 4},
                {"letter": "j", "items": 2},
            ],
        }

    def test_initialise(self, mock_requests_get):
        """Correct initialisation of CategoryBreakdown dataclass."""
        from grand_exchanger.resources.category import CategoryBreakdown, LetterCount

        result = resources.get_category_breakdown(1)

        assert result == CategoryBreakdown(
            alpha=[
                LetterCount(letter="#", items=0),
                LetterCount(letter="a", items=4),
                LetterCount(letter="j", items=2),
            ]
        )

    def test_get_categories(self, mocker):
        """Categories are correctly extracted from HTML."""
        mock = mocker.patch("requests_html.HTMLSession")
        mock.return_value.get.return_value.html.find.return_value = iter(
            [
                mocker.Mock(text="Ammo", attrs={"href": "catalogue?cat=1"}),
                mocker.Mock(text="Food", attrs={"href": "catalogue?cat=2"}),
                mocker.Mock(text="Armour", attrs={"href": "catalogue?cat=3"}),
                mocker.Mock(text="Weapons", attrs={"href": "catalogue?cat=4"}),
            ]
        )

        result = resources.get_categories()
        assert list(result) == [
            (1, "Ammo"),
            (2, "Food"),
            (3, "Armour"),
            (4, "Weapons"),
        ]


class TestItems:
    """Test class for grand_exchanger.resources.items."""

    @pytest.fixture
    def mock_requests_get(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "total": 97,
            "items": [
                {
                    "icon": "",
                    "icon_large": "",
                    "id": 1,
                    "type": "Familiars",
                    "typeIcon": "",
                    "name": "Thing",
                    "description": "A thing",
                    "current": {"trend": "neutral", "price": 100},
                    "today": {"trend": "neutral", "price": 110},
                    "members": "true",
                },
                {
                    "icon": "",
                    "icon_large": "",
                    "id": 2,
                    "type": "Melee weapons - high level",
                    "typeIcon": "",
                    "name": "Sword",
                    "description": "A sword",
                    "current": {"trend": "neutral", "price": "11.3k"},
                    "today": {"trend": "neutral", "price": "24.4m"},
                    "members": "false",
                },
                {
                    "icon": "",
                    "icon_large": "",
                    "id": 3,
                    "type": "Melee weapons - high level",
                    "typeIcon": "",
                    "name": "Another Sword",
                    "description": "Another sword",
                    "current": {"trend": "neutral", "price": "1.8b"},
                    "today": {"trend": "neutral", "price": "43,657"},
                    "members": "false",
                },
            ],
        }

    @pytest.fixture
    def mock_requests_get_invalid(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "total": 97,
            "items": [
                {
                    "icon": "",
                    "icon_large": "",
                    "id": 1,
                    "type": "Familiars",
                    "typeIcon": "",
                    "name": "Thing",
                    "description": "A thing",
                    "current": {"trend": "neutral", "price": "4.2t"},
                    "today": {"trend": "neutral", "price": 110},
                    "members": "true",
                },
            ],
        }

    def test_get_items_page(self, mock_requests_get):
        """Correct instantiation of items from an items page."""
        result = resources.get_items_page(1, "a", 1)

        assert result.total == 97

        item = result.items[0]
        assert item.id == 1
        assert item.name == "Thing"
        assert item.description == "A thing"

        assert item.current.price == 100
        assert item.today.price == 110

        assert item.members is True

        item = result.items[1]

        assert item.current.price == 11300
        assert item.today.price == 24400000

        assert item.members is False

        item = result.items[2]

        assert item.current.price == 1800000000
        assert item.today.price == 43657

    def test_get_items_page_bad_price(self, mock_requests_get_invalid):
        """Unknown price format throws an error."""
        with pytest.raises(marshmallow.ValidationError):
            resources.get_items_page(1, "a", 1)


class TestItemDetails:
    """Test class for grand_exchanger.resources.details."""

    @pytest.fixture
    def mock_requests_get(self, mocker):
        """Fixture for mocking requests.get."""
        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.json.return_value = {
            "item": {
                "icon": "",
                "icon_large": "",
                "id": 21787,
                "type": "Miscellaneous",
                "typeIcon": "",
                "name": "Steadfast boots",
                "description": "A pair of powerful-looking boots.",
                "current": {"trend": "neutral", "price": "5.9m"},
                "today": {"trend": "negative", "price": "- 138.2k"},
                "members": "true",
                "day30": {"trend": "positive", "change": "+0.0%"},
                "day90": {"trend": "negative", "change": "-3.0%"},
                "day180": {"trend": "negative", "change": "-4.0%"},
            }
        }

    @pytest.fixture
    def mock_requests_get_404(self, mocker):
        """Fixture for mocking requests.get."""

        def side_effect():
            raise requests.HTTPError

        mock = mocker.patch("requests.get")
        mock.return_value.__enter__.return_value.raise_for_status.side_effect = (
            side_effect
        )

    def test_get_item_details(self, mock_requests_get):
        """Correct instantiation of ItemDetails dataclass."""
        details = resources.get_item_details(21787)

        item = details.item
        assert item.id == 21787
        assert item.name == "Steadfast boots"
        assert item.type == "Miscellaneous"
        assert item.current.price == 5900000
        assert item.today.price == -138200
        assert item.members is True

    def test_get_item_details_invalid_id(self, mock_requests_get_404):
        """Retrieval of an unknown item causes an error."""
        with pytest.raises(exceptions.NoSuchItemException):
            resources.get_item_details(1)
