"""Tests for commands in the poll group."""
import json

import click.testing
import pytest

from grand_exchanger.cli import poll


@pytest.mark.e2e
class TestPoll:
    """Test class for poll commands."""

    @pytest.fixture
    def runner(self):
        """Fixture for click runner."""
        return click.testing.CliRunner()

    def test_item(self, runner):
        """Test JSON deserialization for the current item price."""
        result = runner.invoke(poll.cli, ["item", "2"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_item_invalid(self, runner):
        """Test ungraceful exit for an non-existent item."""
        result = runner.invoke(poll.cli, ["item", "9999"])

        assert result.exit_code == 1

    def test_category(self, runner):
        """Test JSON deserialization for current item prices in a category."""
        result = runner.invoke(poll.cli, ["category", "38"])

        assert result.exit_code == 0
        for i in result.output.split("\n"):
            if i:
                assert json.loads(i)

    def test_category_invalid(self, runner):
        """Test ungraceful exit for an non-existent category."""
        result = runner.invoke(poll.cli, ["category", "9999"])

        assert result.exit_code == 1
