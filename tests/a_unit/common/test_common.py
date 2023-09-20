"""Tests for the common subpackage."""

from importlib.machinery import ModuleSpec
from unittest.mock import patch

import pytest

from simple.common.common import StatusException, check_install_status, clean_directory

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
    # The pytest fixture create_files will have created file in tmp_path
    # Get a list of the files within tmp_path
    files = [file for file in tmp_path.iterdir()]
    # Print files to the test report for debugging
    if DEBUG:
        print("Files exist:")
        print(*files, sep="\n")
    # Run clean directory function
    clean_directory(tmp_path, FILES)
    # Check if any files exist within tmp_path
    contains_files = any(tmp_path.iterdir())  # False if empty
    # Test that all files have been removed
    assert contains_files is False
    if DEBUG:
        print("Files in tmp_path:")
        # Check again if any files exist within tmp_path
        files = [file for file in tmp_path.iterdir()]
        print(*files, sep="\n")


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_full_install(mock_find_spec, capsys):
    """Test check install status - full install."""
    # Set a full install specification
    full_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/lib/python/site-packages/simple/__init__.py",
    )
    # Set the return value for mocked function
    mock_find_spec.return_value = full_spec
    # Get install status, with mock applied
    result = check_install_status(display=True)
    # Confirm result is as expected
    assert result == "Install"


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_editable(mock_find_spec, capsys):
    """Test check install status - editable."""
    # Set editable develop install specification
    editable_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/user/path/repos/simple/simple/src/simple/__init__.py",
    )
    # Set the mocked function return value
    mock_find_spec.return_value = editable_spec
    # Get install status, with mock applied
    result = check_install_status(display=True)
    assert result == "Editable"


@patch("simple.common.common.find_spec")  # Note the source!
def test_check_install_status_bad_path(mock_find_spec):
    """Test check install status - unknown path."""
    # No output to stdout
    # Set incorrect spec
    bad_spec = ModuleSpec(
        name="simple",
        loader=None,
        origin="/example/user/path/repos/simple/simple/simple/__init__.py",
    )
    # Set the mocked function return value
    mock_find_spec.return_value = bad_spec
    # Get install status, with mock applied
    with pytest.raises(StatusException):
        check_install_status()
