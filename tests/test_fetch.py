import json

import click.testing
import pytest

from grand_exchanger.cli import fetch


@pytest.mark.e2e
class TestFetch:
    @pytest.fixture
    def runner(self):
        return click.testing.CliRunner()

    def test_item_date_succeeds(self, runner):
        result = runner.invoke(fetch.cli, ["-t", "2020-06-06", "item", "-i", "2"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_interval_default_succeeds(self, runner):
        result = runner.invoke(fetch.cli, ["item", "-i", "2"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_interval_succeeds(self, runner):
        result = runner.invoke(
            fetch.cli,
            [
                "-t0",
                "2020-06-06T00:00:00",
                "-t1",
                "2020-08-06T00:00:00",
                "item",
                "-i",
                "2",
            ],
        )

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_interval_upper_succeeds(self, runner):
        result = runner.invoke(
            fetch.cli, ["-t1", "2020-08-06T00:00:00", "item", "-i", "2"]
        )

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_interval_lower_succeeds(self, runner):
        result = runner.invoke(
            fetch.cli, ["-t0", "2020-06-06T00:00:00", "item", "-i", "2"]
        )

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_bad_arguments(self, runner):
        result = runner.invoke(
            fetch.cli,
            [
                "-t",
                "2020-06-06",
                "-t0",
                "2020-06-06T00:00:00",
                "-t1",
                "2020-08-06T00:00:00",
                "item",
                "-i",
                "2",
            ],
        )

        assert result.exit_code == 1

    def test_item_fails(self, runner):
        result = runner.invoke(fetch.cli, ["item", "-i", "9999"])

        assert result.exit_code == 1

    def test_category(self, runner):
        result = runner.invoke(fetch.cli, ["category", "-i", "38"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_category_date_succeeds(self, runner):
        result = runner.invoke(fetch.cli, ["-t", "2020-06-06", "category", "-i", "38"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_category_fails(self, runner):
        result = runner.invoke(fetch.cli, ["category", "-i", "9999"])

        assert result.exit_code == 1
