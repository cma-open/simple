"""Tests for the config subpackage."""

from importlib.resources import files
from pathlib import PosixPath
from unittest.mock import patch

from simple.config.reader import (
    return_datadir,
    return_inputs,
    return_outputs,
    return_verbosity,
)
from simple.definitions import RESOURCES

TEST_CONFIGFILE = files(RESOURCES) / "test_config.ini"

# Note these integration tests run against static test files
# This allows full process to be tested


# Patch out functions at the location used, not where defined
@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_datadir_full_install(mock_install_status):
    """Test return_datadir function."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Runs tests using the test_config.ini file
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        # Get datadir (will always be a Path object)
        datadir = return_datadir()
        # Print further info for verbose editable installs
        if return_verbosity():
            print(f"Datadir is: {datadir}")
        expected = PosixPath("/alt/home/user/temp")
        assert datadir == expected
    # Editable and home ~ directory based confg options not tested here, see unit tests


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_outputs_full_install(mock_install_status):
    """Test return_outputs function."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Runs tests using the test_config.ini file
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        datadir = return_outputs()
        # Print further info for verbose editable installs
        if return_verbosity():
            print(f"Datadir is: {datadir}")
        expected = PosixPath("/alt/home/user/temp/data/test_outputs")
        assert datadir == expected
    # Editable and home dir based confg options not tested here, see unit tests


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_inputs_full_install(mock_install_status):
    """Test return_inputs function."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Runs tests using the test_config.ini file
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        datadir = return_inputs()
        expected = PosixPath("/alt/home/user/temp/data/test_inputs")
        assert datadir == expected
    # Editable and home dir based confg options not tested here, see unit tests


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_scratch_full_install(mock_install_status):
    """Test return_inputs function."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Runs tests using the test_config.ini file
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        datadir = return_inputs()
        expected = PosixPath("/alt/home/user/temp/data/test_inputs")
        assert datadir == expected
    # Editable and home dir based config options not tested here, see unit tests
