"""Integration tests for the log module."""

import logging

from simple.logger.log import create_config_logger


def test_create_config_logger(tmp_path):
    """Test the create_config_logger function."""
    test_log_path = tmp_path / "test.log"
    test_logger = create_config_logger(
        log_path=test_log_path, logger_name="TestConfigLogIntegration"
    )
    test_logger.info("test")
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert len(test_logger.handlers) == 1
    assert "FileHandler" in str(test_logger.handlers[0])
    assert test_log_path.is_file()
    assert test_logger.isEnabledFor(logging.DEBUG)
