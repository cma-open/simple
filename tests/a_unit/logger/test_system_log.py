"""Unit tests for the log module."""

import logging

from simple.logger.log import (
    add_system_console_handler,
    add_system_log_file_handler,
    create_system_logger,
)


def test_add_system_console_handler():
    """Test add system console handler to a logger."""
    test_logger = logging.getLogger("console_handler_test")
    add_system_console_handler(logger=test_logger)

    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)


def test_add_system_log_file_handler(tmp_path):
    """Test the add_system_log_file_handler function."""
    test_log_path = tmp_path / "test.log"
    test_logger = logging.getLogger("system_log_file_handler_test")
    add_system_log_file_handler(logger=test_logger, log_path=test_log_path)

    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    print(test_logger.handlers)


def test_create_system_logger(tmp_path):
    """Test the create_system_logger function."""
    test_log_path = tmp_path / "test.log"
    test_logger = create_system_logger(log_path=test_log_path)
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)
    # Note cant test with isinstance due to inheritance
    assert isinstance(test_logger.handlers[1], logging.FileHandler)
    assert "FileHandler" in str(test_logger.handlers[1])
    assert "FileHandler" and "StreamHandler" in str(test_logger.handlers)
    print(test_logger.handlers)
    assert test_log_path.is_file()
    print(test_logger)
