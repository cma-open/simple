"""Tests for the common subpackage."""

from importlib.machinery import ModuleSpec
from unittest.mock import patch

import pytest

from simple.common.common import check_install_status, clean_directory

# List of data files generated and used within the system.
# TODO move to use single source of FILES
FILES = ["test.nc", "other.nc", "more.txt"]

DEBUG = False


@pytest.fixture
def create_files(tmp_path):
    """Create test files."""
    # Fixture to create named files from list int tmp_path
    for file in FILES:
        filepath = tmp_path / file
        filepath.touch()


def test_clean_directory(tmp_path, create_files):
    """Test clean_directory function."""
    files = [file for file in tmp_path.iterdir()]
    # print files to the test report for debugging
    if DEBUG:
        print("Files exist:")
        print(*files, sep="\n")
    # clean directory
    clean_directory(tmp_path, FILES)
    contains_files = any(tmp_path.iterdir())  # False if empty
    assert contains_files is False
    if DEBUG:
        print("Files in tmp_path:")
        files = [file for file in tmp_path.iterdir()]
        print(*files, sep="\n")


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_user(mock_find_spec, capsys):
    """Test check install status - user."""
    # set user install
    user_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/lib/python/site-packages/simple/__init__.py",
    )
    mock_find_spec.return_value = user_spec
    result = check_install_status(display=True)
    assert result == "User"
    # test output to stdout
    captured = capsys.readouterr()
    expected = (
        "User install into site-packages at: "
        "/example/lib/python/site-packages/simple/__init__.py"
    )
    assert expected in captured.out


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_editable(mock_find_spec, capsys):
    """Test check install status - editable."""
    # set editable develop install
    editable_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/user/path/repos/simple/simple/src/simple/__init__.py",
    )
    mock_find_spec.return_value = editable_spec
    result = check_install_status(display=True)
    assert result == "Editable"
    # test output to stdout
    captured = capsys.readouterr()
    expected = (
        "Editable install at: "
        "/example/user/path/repos/simple/simple/src/simple/__init__.py"
    )
    assert expected in captured.out


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_bad_path(mock_find_spec):
    """Test check install status - unknown path."""
    # not output to stdout to test
    # set incorrect spec
    bad_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/user/path/repos/simple/simple/simple/__init__.py",
    )
    mock_find_spec.return_value = bad_spec
    result = check_install_status()
    assert result == "Unknown path or not installed"
