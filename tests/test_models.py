from datetime import datetime

import pytest

from grand_exchanger import models, resources


class TestItem:
    @pytest.fixture
    def mock_get_historical_prices(self, mocker):
        mock = mocker.patch("grand_exchanger.resources.get_historical_prices")
        mock.return_value.list_daily_prices.return_value = iter(
            [
                (datetime(2020, 7, 3), 113),
                (datetime(2020, 7, 2), 111),
                (datetime(2020, 7, 1), 108),
            ]
        )

    def test_initialise(self):
        item = models.Item(1, "Thing", False)

        assert item.id == 1
        assert item.name == "Thing"
        assert item.members is False

    def test_get_historical_prices(self, mock_get_historical_prices):
        item = models.Item(1, "Thing", False)

        assert list(item.get_historical_prices()) == [
            (datetime(2020, 7, 3), 113),
            (datetime(2020, 7, 2), 111),
            (datetime(2020, 7, 1), 108),
        ]


class TestCategory:
    def test_initialise(self):
        category = models.Category(1, "Ammo")

        assert category.id == 1
        assert category.name == "Ammo"

    @pytest.fixture
    def mock_resources_get_category_breakdown(self, mocker):
        mock = mocker.patch("grand_exchanger.resources.get_category_breakdown")
        mock.return_value = resources.CategoryBreakdown(
            alpha=[resources.LetterCount("#", 2), resources.LetterCount("a", 3)]
        )

    @pytest.fixture
    def mock_resources_get_items_page(self, mocker):
        from grand_exchanger.resources.items import Item, PriceTrend

        def get_items_page(category_id, letter, page):
            if page > 1:
                return resources.Items(total=4, items=[])
            else:
                if letter == "%23":
                    return resources.Items(
                        total=4,
                        items=[
                            Item(
                                1,
                                "2handed sword",
                                "",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                        ],
                    )
                elif letter == "a":
                    return resources.Items(
                        total=4,
                        items=[
                            Item(
                                2,
                                "armadyl crossbow",
                                "",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                            Item(
                                3,
                                "adamant sword",
                                "",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                            Item(
                                4,
                                "adamant spear",
                                "",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                        ],
                    )
                else:
                    return resources.Items(total=4, items=[])

        mock = mocker.patch("grand_exchanger.resources.get_items_page")
        mock.side_effect = get_items_page

    def test_get_item_current_prices(
        self, mock_resources_get_category_breakdown, mock_resources_get_items_page
    ):
        category = models.Category(1, "Ammo")
        assert list(category.get_item_current_prices()) == [
            (models.Item(1, "2handed sword", False), 113),
            (models.Item(2, "armadyl crossbow", False), 113),
            (models.Item(3, "adamant sword", False), 113),
            (models.Item(4, "adamant spear", False), 113),
        ]

    def test_get_items(
        self, mock_resources_get_category_breakdown, mock_resources_get_items_page
    ):
        category = models.Category(1, "Ammo")
        assert list(category.get_items()) == [
            models.Item(1, "2handed sword", False),
            models.Item(2, "armadyl crossbow", False),
            models.Item(3, "adamant sword", False),
            models.Item(4, "adamant spear", False),
        ]


class TestPriceMeasurement:
    @pytest.fixture
    def item(self):
        return models.Item(1, "Thing", False)

    @pytest.fixture
    def category(self):
        return models.Category(1, "Ammo")

    def test_initialise(self, item, category):
        measurement = models.PriceMeasurement(item, category, 100, datetime(2020, 1, 1))

        assert measurement.item
        assert measurement.category
        assert measurement.price == 100
        assert measurement.dt == datetime(2020, 1, 1)

    def test_to_dict(self, item, category):
        measurement = models.PriceMeasurement(item, category, 100, datetime(2020, 1, 1))

        assert measurement.to_dict() == {
            "measurement": "price",
            "tags": {"category_id": 1, "item_id": 1, "members": False},
            "time": "2020-01-01T00:00:00Z",
            "fields": {"value": 100},
        }
