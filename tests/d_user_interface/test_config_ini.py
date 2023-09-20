"""Tests for the config.ini file."""

# Note
# Kept here ot illustrate potential test content
# Other options include
# - use of a validation schema
# - validation within a config reader class

import configparser
from pathlib import Path

from simple.definitions import PACKAGE_DIR


def test_valid_config_ini_file():
    """Test the config file is valid."""
    # Set path to user-edited config file
    configfile = f"{PACKAGE_DIR}/config.ini"
    # Check file exists
    assert Path(configfile).is_file()
    # Create parser
    config = configparser.ConfigParser()
    # Read the config file
    user_config = config.read(configfile)
    # Confirm read file and returns list
    assert isinstance(user_config, list)
    # Test the file has required config sections
    assert "LOGS" in config.sections()
    assert "DATADIR" in config.sections()


def test_config_ini_file_values():
    """Test the config file content."""
    # Set path to user-edited config file
    configfile = f"{PACKAGE_DIR}/config.ini"
    # Create parser
    config = configparser.ConfigParser()
    # Read the config file
    config.read(configfile)
    # Get values
    inputs = config.get("DATADIR", "INPUTS")
    outputs = config.get("DATADIR", "OUTPUTS")
    scratch = config.get("DATADIR", "SCRATCH")
    system_logs = config.get("DATADIR", "INPUTS")
    config_logs = config.get("DATADIR", "OUTPUTS")
    log_level = config.get("DATADIR", "SCRATCH")
    # Test section values are non-empty strings
    values_list = [inputs, outputs, scratch, system_logs, config_logs, log_level]
    for value in values_list:
        assert isinstance(value, str) and len(value) > 0
