"""Tests for the cli module."""
import pytest

from simple.cli import cli_data, cli_entry_point


# TODO to mock or not, ideally don't actually want to call cli
def test_cli_entry_point(capsys):
    """Test cli entry point for tool CLI-SIMPLE."""
    argv = ["2", "2"]
    out = cli_entry_point(argv=argv)
    assert out is None
    # check stdout output
    captured = capsys.readouterr()
    expected = "['4.000005', '4.000005']\n"
    # assert expected in captured.out
    assert captured.out == expected


def test_cli_data_version(capsys):
    """Test cli entry point for tool CREATE-DATA."""
    argv = ["--version"]
    with pytest.raises(SystemExit):
        cli_data(argv=argv)
        captured = capsys.readouterr()
        expected = "CREATE-DATA"
        assert expected in captured.out


# TODO START add more tests - review and add mocks, compare to end to end tests
