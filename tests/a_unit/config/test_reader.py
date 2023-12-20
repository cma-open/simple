"""Tests for the config subpackage."""

from importlib.resources import files
from pathlib import Path, PosixPath
from unittest.mock import patch

import pytest

from simple.config.reader import (
    ConfigException,
    log_config,
    return_datadir,
    return_inputs,
    return_log_level,
    return_logs_dir,
    return_outputs,
    return_scratch,
)
from simple.definitions import RESOURCES
from simple.setup.system_setup import setup_directories

TEST_CONFIGFILE = files(RESOURCES) / "test_config.ini"


# Patch out functions at the location used, not where defined
@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_datadir_editable(mock_install_status):
    """Test return_datadir function."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Editable"
    # Mock the ROOT_DIR constant
    mock_root = Path("/home/example/user/simple/simple/src")
    with patch("simple.config.reader.ROOT_DIR", mock_root):
        # Run function, with mocked content
        datadir = return_datadir()
        assert datadir == PosixPath("/home/example/user/simple/simple")


# Patch out functions at the location used, not where defined
@patch("simple.config.reader.Path.expanduser")
@patch("simple.config.reader.config.get")
@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_datadir_full_home(mock_install_status, mock_get, mock_user):
    """Test return_datadir function with home location."""
    # Mock out check install status and config.get
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Set return value for mocked .get
    mock_get.return_value = "~"
    # Set return value for mocked .expanduser method
    mock_user.return_value = "/example/directory/temp"
    # Run function, with mocked content
    datadir = return_datadir()
    assert datadir == "/example/directory/temp"


@patch("simple.config.reader.config.get")
@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_datadir_full_conf(mock_install_status, mock_get):
    """Test return_datadir function with user set location."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Set return value for mocked .get function
    mock_get.return_value = "/home/example/user/temp"
    # Run function, with mocked content
    datadir = return_datadir()
    assert datadir == "/home/example/user/temp"


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_return_datadir_raises(mock_install_status):
    """Test return_datadir function with user set location."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "other_bad_value"
    with pytest.raises(ConfigException):
        # Run function, with mocked content
        return_datadir()


# Test return_outputs (install / editable)
@patch("simple.config.reader.return_datadir")
def test_return_outputs_editable(mock_datadir):
    """Test return_outputs function with test config.ini file."""
    mock_datadir.return_value = PosixPath("/home/example/user/simple/simple")
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_outputs()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/simple/simple/data/test_outputs")
        assert outputs == expected


@patch("simple.config.reader.return_datadir")
def test_return_outputs_install(mock_datadir):
    """Test return_outputs function with test config.ini file."""
    mock_datadir.return_value = "/home/example/user"
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_outputs()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/data/test_outputs")
        assert outputs == expected


# Test return_inputs (install / editable)
@patch("simple.config.reader.return_datadir")
def test_return_inputs_editable(mock_datadir):
    """Test return_inputs function with test config.ini file."""
    mock_datadir.return_value = PosixPath("/home/example/user/simple/simple")
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_inputs()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/simple/simple/data/test_inputs")
        assert outputs == expected


@patch("simple.config.reader.return_datadir")
def test_return_inputs_install(mock_datadir):
    """Test return_inputs function with test config.ini file."""
    mock_datadir.return_value = "/home/example/user"
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_inputs()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/data/test_inputs")
        assert outputs == expected


# Test return_scratch (install / editable)


@patch("simple.config.reader.return_datadir")
def test_return_scratch_editable(mock_datadir):
    """Test return_scratch function with test config.ini file."""
    mock_datadir.return_value = PosixPath("/home/example/user/simple/simple")
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_scratch()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/simple/simple/data/test_scratch")
        assert outputs == expected


@patch("simple.config.reader.return_datadir")
def test_return_scratch_install(mock_datadir):
    """Test return_scratch function with test config.ini file."""
    mock_datadir.return_value = "/home/example/user"
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_scratch()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/data/test_scratch")
        assert outputs == expected


# Test return_logs_dir (install / editable)


@patch("simple.config.reader.return_datadir")
def test_return_logs_dir_editable(mock_datadir):
    """Test return_logs_dir function with test config.ini file."""
    mock_datadir.return_value = PosixPath("/home/example/user/simple/simple")
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_logs_dir()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/simple/simple/test_logs/")
        assert outputs == expected


@patch("simple.config.reader.return_datadir")
def test_return_logs_install(mock_datadir):
    """Test return_system_logs function with test config.ini file."""
    mock_datadir.return_value = "/home/example/user"
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_logs_dir()  # Note always returns PosixPath, not str
        expected = PosixPath("/home/example/user/test_logs/")
        assert outputs == expected


def test_return_log_level():
    """Test return_log_level function with test config.ini file."""
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        outputs = return_log_level()
        expected = "debug"
        assert outputs == expected


# Test via creating dirs into tmp_path
# Mock out the main return_datadir root dir with tmp_path
@patch("simple.config.reader.return_datadir")
def test_setup_directories(mock_datadir, tmp_path):
    """Test setup_directories based on configfile."""
    mock_datadir.return_value = tmp_path
    with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
        # Create dirs, as specified by config file
        setup_directories(datadir_root_path=tmp_path)
        # Check expected files exist in the main root/data directory
        expected_data_dirs = ["test_inputs", "test_outputs", "test_scratch"]
        for subdir in expected_data_dirs:
            subdir_path = tmp_path / "data" / subdir
            assert subdir_path.is_dir()
        # Check the logs dir has been created at root/logs
        expected_logs_dir = "test_logs"
        assert (tmp_path / expected_logs_dir).is_dir()


# TODO !
# def test_log_config(tmp_path):
#     "Test log config based on configfile."
#     with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
#         # Log the config file
#         log = log_config(log_dir_path=tmp_path)
#         # Check the logs file has been created
#         expected_log_file = "config.log"
#         #assert (tmp_path / expected_log_file).is_file()
#         print(log)
#         assert log.is_file()


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_log_config_editable(mock_install_status, tmp_path):
    """Test log config based on configfile."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Editable"
    # Log the config file
    log = log_config(log_dir_path=tmp_path)
    # Check the logs file has been created
    expected_log_file = "config.log"
    expected_log_file_path = tmp_path / expected_log_file
    # Check file exists and location is as expected
    assert expected_log_file_path.is_file()
    assert log == expected_log_file_path


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_log_config_install(mock_install_status, tmp_path):
    """Test log config based on configfile."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "Install"
    # Log the config file
    log = log_config(log_dir_path=tmp_path)
    # Check the logs file has been created
    expected_log_file = "config.log"
    expected_log_file_path = tmp_path / expected_log_file
    # Check file exists and location is as expected
    assert expected_log_file_path.is_file()
    assert log == expected_log_file_path


@patch("simple.config.reader.check_install_status")  # Note the source!
def test_log_config_raises(mock_install_status, tmp_path):
    """Test log config based on configfile."""
    # Mock out check install status
    # Set the return value for mocked function
    mock_install_status.return_value = "other-bad-value"
    with pytest.raises(ConfigException):
        # Log the config file
        log_config(log_dir_path=tmp_path)
