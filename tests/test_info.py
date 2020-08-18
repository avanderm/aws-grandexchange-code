import click.testing
import pytest

from grand_exchanger.cli import info


@pytest.mark.e2e
class TestInfo:
    @pytest.fixture
    def runner(self):
        return click.testing.CliRunner()

    def test_ls(self, runner):
        result = runner.invoke(info.cli, ["ls"])
        assert result.exit_code == 0

    def test_item(self, runner):
        result = runner.invoke(info.cli, ["item", "-i", "2"])
        assert result.exit_code == 0

    def test_item_invalid(self, runner):
        result = runner.invoke(info.cli, ["item", "-i", "0"])
        assert result.exit_code == 1

    def test_category(self, runner):
        result = runner.invoke(info.cli, ["category", "-i", "38"])
        assert result.exit_code == 0

    def test_category_invalid(self, runner):
        result = runner.invoke(info.cli, ["category", "-i", "9999"])
        assert result.exit_code == 1
