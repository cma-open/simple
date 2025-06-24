"""Integration tests for the log module - system logs."""

import logging

from simple.logger.log import create_system_logger


# Tests for create_system_logger function
# Different tests required for default logger name at package root, or custom name
def test_create_system_logger_custom_name(tmp_path):
    """Test the create_system_logger function - with custom name."""
    # Create test log file in pytest temp path
    test_log_path = tmp_path / "test.log"
    # Create system logger with specified name
    test_logger = create_system_logger(
        log_path=test_log_path,
        logger_name="test_logger",
        file_handler_name="TestFileHandler",
    )
    # Test for expected type and presence of handlers
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert len(test_logger.handlers) == 1  # Only 1 handler
    # For non default named system logger then only log file handlers will exist
    # No stream handler, because there is no access to default system logger via init
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    assert "StreamHandler" not in str(test_logger.handlers)
    # Test log file exists
    assert test_log_path.is_file()
    # Test expected name has been set
    assert test_logger.name == "test_logger"
    # Test handler name
    assert test_logger.handlers[0].name == "TestFileHandler"
    # Test expected logger level has been set DEBUG = 10
    assert test_logger.level == 10
    # Test expected handler level has been set DEBUG = 10
    assert test_logger.handlers[0].level == 10


def test_create_system_logger_default_name(tmp_path):
    """Test the create_system_logger function."""
    # Create test log file in pytest temp path
    test_log_path = tmp_path / "test.log"
    # Create system logger
    # As a default this will use package log name
    # Therefore this will access default system logger created via init
    test_logger = create_system_logger(log_path=test_log_path)
    # Test for expected logger type, handler, file, name and level
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)
    # Note cant test with isinstance due to inheritance
    assert isinstance(test_logger.handlers[1], logging.FileHandler)
    assert "FileHandler" and "StreamHandler" in str(test_logger.handlers)
    # Don't test for number of handlers, system file handler will be added to
    # Test log file exists
    assert test_log_path.is_file()
    # Test expected name has been set
    assert test_logger.name == "simple"  # package name logger
    # Test expected log level has been set DEBUG = 10
    assert test_logger.level == 10
    # Collect the current handler names
    handler_names = [handler.name for handler in test_logger.handlers]
    # Check expected handler names are present in logger handlers
    assert "SystemConsoleHandler" in handler_names
    assert "SystemFileHandler" in handler_names
    # Test handlers have the expected log levels set
    assert [
        handler.level == 20
        for handler in test_logger.handlers
        if handler.name == "SystemConsoleHandler"
    ]
    assert [
        handler.level == 10
        for handler in test_logger.handlers
        if handler.name == "SystemFileHandler"
    ]
