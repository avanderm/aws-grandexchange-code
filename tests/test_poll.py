import json

import click.testing
import pytest

from grand_exchanger.cli import poll


@pytest.mark.e2e
class TestPoll:
    @pytest.fixture
    def runner(self):
        return click.testing.CliRunner()

    def test_item(self, runner):
        result = runner.invoke(poll.cli, ["item", "-i", "2"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_invalid(self, runner):
        result = runner.invoke(poll.cli, ["item", "-i", "9999"])

        assert result.exit_code == 1

    def test_category(self, runner):
        result = runner.invoke(poll.cli, ["category", "-i", "38"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_category_invalid(self, runner):
        result = runner.invoke(poll.cli, ["category", "-i", "9999"])

        assert result.exit_code == 1
