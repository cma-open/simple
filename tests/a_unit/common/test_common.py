"""Tests for the common subpackage."""

from importlib.machinery import ModuleSpec
from unittest.mock import patch

import pytest

from simple.common.common import (
    StatusException,
    check_install_status,
    clean_directory,
    debug_loggers,
)
from simple.config.reader import return_verbosity

# List of data files generated and used within the system.
# TODO move to use single source of FILES
FILES = ["test.nc", "other.nc", "more.txt"]


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
    # Print files to the test report for debugging if verbose editable install
    if return_verbosity():
        print("Files exist:")
        print(*files, sep="\n")
    # Run clean directory function
    clean_directory(tmp_path, FILES)
    # Check if any files exist within tmp_path
    contains_files = any(tmp_path.iterdir())  # False if empty
    # Test that all files have been removed
    assert contains_files is False
    # Print files to the test report for debugging if verbose editable install
    if return_verbosity():
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


def test_debug_loggers(capsys):
    """List current available loggers for use in debugging."""
    # Kept for training use as useful to show list of loggers by name
    debug_loggers()
    # Capture prints
    captured = capsys.readouterr()
    # Split returned strinng into strings by newlines
    logger_lines = captured.out.splitlines()
    # Check that each printed line refers to a Logger
    for logger in logger_lines:
        assert "Logger" in logger
    # Expect at least three seperate loggers
    number_loggers = len(captured.out.splitlines())
    print(f"There are {number_loggers} Loggers in use by the system")
    assert number_loggers > 3
    # Run debug loggers again so that print also shows in main test report
    # Required due to capturing of first output above for use in the test
    debug_loggers()
