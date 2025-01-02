"""Tests for the status module."""

import logging
from unittest.mock import patch

from simple.definitions import PACKAGE
from simple.status.checks import confirm_config, show_loggers, show_version


def test_show_version(caplog):
    """Test show_version logs the correct system package version."""
    system_version = "1.0.0"  # Example version

    with patch("simple.status.checks.version", return_value=system_version):
        with caplog.at_level(logging.INFO):
            show_version()
            assert f"System version: {PACKAGE}-{system_version}" in caplog.text


def test_confirm_config():
    """Test for the confirm_config function."""
    confirm_config()
    # TODO


def test_show_loggers(capfd):
    """Test show_loggers prints the available loggers."""
    # Create a test logger to ensure there's at least one logger
    test_logger = logging.getLogger("test_logger")
    test_logger.setLevel(logging.INFO)

    show_loggers()

    # Capture the output
    captured = capfd.readouterr()
    output = captured.out

    # Check if the test logger is in the output
    assert "test_logger" in output
    # Check some key expected logs are present
    assert "ConfigLog" in output
    assert "simple" in output
    assert "---" in output  # Check for the separator lines
