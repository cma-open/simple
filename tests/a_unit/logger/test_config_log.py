"""Unit tests for the log module."""

import logging

from simple.logger.log import add_config_log_file_handler, create_config_logger


def test_add_config_log_file_handler(tmp_path):
    """Test the add_config_log_file_handler function."""
    test_log_path = tmp_path / "test.log"
    test_logger = logging.getLogger("config_log_file_handler_test")
    add_config_log_file_handler(logger=test_logger, log_path=test_log_path)
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    assert test_log_path.is_file()


def test_create_config_logger(tmp_path):
    """Test the create_config_logger function."""
    test_log_path = tmp_path / "test.log"
    test_logger = create_config_logger(log_path=test_log_path)
    test_logger.info("test")
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert "FileHandler" in str(test_logger.handlers[0])
    assert test_log_path.is_file()
