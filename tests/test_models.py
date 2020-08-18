from datetime import datetime

import pytest

from grand_exchanger import exceptions, models


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

    @pytest.fixture
    def mock_get_item_details(self, mocker):
        from grand_exchanger.resources.details import ItemDetails
        from grand_exchanger.resources.common import Item, PriceTrend

        mock = mocker.patch("grand_exchanger.resources.get_item_details")
        mock.return_value = ItemDetails(
            item=Item(
                id=1,
                name="Thing",
                description="",
                type="Swords",
                current=PriceTrend("positive", 100),
                today=PriceTrend("positive", 10),
                members=True,
            )
        )

    def test_initialise(self):
        item = models.Item(1, "Thing", "Swords", False, 100)

        assert item.id == 1
        assert item.name == "Thing"
        assert item.members is False
        assert item.price == 100

    def test_to_str(self):
        item = models.Item(1, "Thing", "Swords", False, 100)

        assert (
            item.to_str()
            == """
        Thing (1):
        category: Swords
        members: False

        price: 100
        """
        )

    def test_get_historical_prices(self, mock_get_historical_prices):
        item = models.Item(1, "Thing", "Swords", False, 100)

        assert list(item.get_historical_prices()) == [
            (datetime(2020, 7, 3), 113),
            (datetime(2020, 7, 2), 111),
            (datetime(2020, 7, 1), 108),
        ]

    def test_get(self, mock_get_item_details):
        item = models.Item.get(1)

        assert item.id == 1
        assert item.price == 100


class TestCategory:
    def test_initialise(self):
        category = models.Category(1, "Swords")

        assert category.id == 1
        assert category.name == "Swords"

    @pytest.fixture
    def mock_resources_get_category_breakdown(self, mocker):
        from grand_exchanger.resources.category import CategoryBreakdown, LetterCount

        mock = mocker.patch("grand_exchanger.resources.get_category_breakdown")
        mock.return_value = CategoryBreakdown(
            alpha=[LetterCount("#", 2), LetterCount("a", 3)]
        )

    @pytest.fixture
    def mock_resources_get_items_page(self, mocker):
        from grand_exchanger.resources.items import Items
        from grand_exchanger.resources.common import Item, PriceTrend

        def get_items_page(category_id, letter, page):
            if page > 1:
                return Items(total=4, items=[])
            else:
                if letter == "%23":
                    return Items(
                        total=4,
                        items=[
                            Item(
                                1,
                                "2handed sword",
                                "",
                                "Swords",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                        ],
                    )
                elif letter == "a":
                    return Items(
                        total=4,
                        items=[
                            Item(
                                2,
                                "armadyl crossbow",
                                "",
                                "Swords",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                            Item(
                                3,
                                "adamant sword",
                                "",
                                "Swords",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                            Item(
                                4,
                                "adamant spear",
                                "",
                                "Swords",
                                current=PriceTrend(trend="", price=100),
                                today=PriceTrend(trend="", price=113),
                                members=False,
                            ),
                        ],
                    )
                else:
                    return Items(total=4, items=[])

        mock = mocker.patch("grand_exchanger.resources.get_items_page")
        mock.side_effect = get_items_page

    def test_get_items(
        self, mock_resources_get_category_breakdown, mock_resources_get_items_page
    ):
        category = models.Category(1, "Not Swords")
        assert list(category.get_items()) == [
            models.Item(1, "2handed sword", "Not Swords", False, 100),
            models.Item(2, "armadyl crossbow", "Not Swords", False, 100),
            models.Item(3, "adamant sword", "Not Swords", False, 100),
            models.Item(4, "adamant spear", "Not Swords", False, 100),
        ]

    @pytest.fixture
    def mock_resources_get_categories(self, mocker):
        mock = mocker.patch("grand_exchanger.resources.get_categories")
        mock.return_value = iter([(1, "Ammo"), (2, "Swords"), (3, "Shields")])

    def test_get_categories(self, mock_resources_get_categories):
        categories = models.Category.get_categories()

        assert list(categories) == [
            models.Category(1, "Ammo"),
            models.Category(2, "Swords"),
            models.Category(3, "Shields"),
        ]

    def test_get(self, mock_resources_get_categories):
        category = models.Category.get(1)

        assert category.id == 1
        assert category.name == "Ammo"

    def test_get_fail(self, mock_resources_get_categories):
        with pytest.raises(exceptions.NoSuchCategoryException):
            models.Category.get(4)

    def test_get_category_for_item(self, mock_resources_get_categories):
        item = models.Item(1, "Thing", "Swords", False, 100)
        category = models.Category.get_category_for_item(item)

        assert category.id == 2
        assert category.name == "Swords"

    def test_get_category_for_item_fail(self, mock_resources_get_categories):
        item = models.Item(1, "Thing", "Schwartz", False, 100)
        with pytest.raises(exceptions.NoSuchCategoryException):
            models.Category.get_category_for_item(item)


class TestPriceMeasurement:
    @pytest.fixture
    def item(self):
        return models.Item(1, "Thing", "Swords", False, 114)

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
            "tags": {"category": "Ammo", "item_id": 1, "members": False},
            "time": "2020-01-01T00:00:00Z",
            "fields": {"value": 100},
        }
