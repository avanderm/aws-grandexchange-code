from datetime import datetime

import marshmallow
import pytest

from grand_exchanger import resources


class TestGraph:
    @pytest.fixture
    def expected_json_response(self):
        return {
            "daily": {"1595808000000": 100, "1595721600000": 120, "1595635200000": 110},
            "average": {
                "1595808000000": 100,
                "1595721600000": 110,
                "1595635200000": 104,
            },
        }

    def test_initialise(self, expected_json_response):
        price_history = resources.GraphSchema.load(expected_json_response)

        assert price_history == resources.Graph(
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

    def test_initialise_bad_timestamp(self, expected_json_response):
        expected_json_response["daily"]["not_an_epoch"] = 100

        with pytest.raises(marshmallow.ValidationError):
            resources.GraphSchema.load(expected_json_response)

    def test_list_daily_prices(self):
        price_history = resources.Graph(
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
        price_history = resources.Graph(
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


class TestCategory:
    @pytest.fixture
    def expected_json_response(self):
        return {
            "types": [],
            "alpha": [
                {"letter": "#", "items": 0},
                {"letter": "a", "items": 4},
                {"letter": "j", "items": 2},
            ],
        }

    def test_initialise(self, expected_json_response):
        category = resources.CategorySchema.load(expected_json_response)

        assert category == resources.Category(
            alpha=[
                resources.LetterCount(letter="#", items=0),
                resources.LetterCount(letter="a", items=4),
                resources.LetterCount(letter="j", items=2),
            ]
        )


class TestItems:
    @pytest.fixture
    def expected_json_response(self):
        return {
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

    def test_initialise(self, expected_json_response):
        items = resources.ItemsSchema.load(expected_json_response)

        assert items.total == 97

        item = items.items[0]
        assert item.id == 1
        assert item.name == "Thing"
        assert item.description == "A thing"

        assert item.current.price == 100
        assert item.today.price == 110

        assert item.members is True

        item = items.items[1]

        assert item.current.price == 11300
        assert item.today.price == 24400000

        assert item.members is False

        item = items.items[2]

        assert item.current.price == 1800000000
        assert item.today.price == 43657

    def test_initialise_bad_price(self, expected_json_response):
        expected_json_response["items"][0]["current"]["price"] = "34.5t"

        with pytest.raises(marshmallow.ValidationError):
            resources.ItemsSchema.load(expected_json_response)
