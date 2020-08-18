import click.testing
import pytest

from grand_exchanger import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_help_succeeds(runner):
    result = runner.invoke(console.cli, ["--help"])
    assert result.exit_code == 0


def test_sub_help_succeeds(runner):
    result = runner.invoke(console.cli, ["info", "--help"])
    assert result.exit_code == 0
