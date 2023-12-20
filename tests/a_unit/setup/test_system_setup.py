"""Tests for the system setup module."""

from unittest.mock import patch

from simple.setup.system_setup import setup_directories

# log_config, setup_system_log


# Test create required subdirectories
# Mock out paths normally set in config
# Patch out functions at the location used, not where defined
@patch("simple.setup.system_setup.return_logs_dir")  # Note the source!
@patch("simple.setup.system_setup.return_scratch")  # Note the source!
@patch("simple.setup.system_setup.return_outputs")  # Note the source!
@patch("simple.setup.system_setup.return_inputs")  # Note the source!
def test_setup_directories(
    mock_inputs, mock_outputs, mock_scratch, mock_logs, tmp_path
):
    """Test setup of system directories."""
    # Set the return value for mocked functions
    mock_inputs.return_value = "inputs"
    mock_outputs.return_value = "outputs"
    mock_scratch.return_value = "scratch"
    mock_logs.return_value = "logs"
    setup_directories(datadir_root_path=tmp_path)
    assert (tmp_path / "inputs").is_dir()
    assert (tmp_path / "outputs").is_dir()
    assert (tmp_path / "scratch").is_dir()
    assert (tmp_path / "logs").is_dir()


def test_log_config():
    """Test for log_config function."""

    # mock out inputs

    # log_config()

    # check files were created
    # check content
    # TODO add test content
    # START HERE >>>>>>>>>>>>>>>>>>>>>>>>>


def test_setup_system_log():
    """Test for setup_system_log."""
    # setup_system_log()
    # needs thought here
    # does this work?
    # or move setup_system_log to init?
    # however its difficult because it has to read from config to work ?
    # check init


def test_update_system_log():
    """Test for update_system_log."""


def test_system_setup():
    """Test system setup."""
