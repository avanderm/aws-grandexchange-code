from datetime import datetime

import pytest

from grand_exchanger import models


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
