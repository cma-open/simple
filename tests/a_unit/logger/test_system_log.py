"""Unit tests for the log module."""

import logging
from unittest.mock import patch

from simple.logger.log import (
    add_system_console_handler,
    add_system_log_file_handler,
    create_system_logger,
)


def test_add_system_console_handler():
    """Test add system console handler to a logger."""
    # Create a test logger
    test_logger = logging.getLogger("console_handler_test")
    # Add handler to the logger
    add_system_console_handler(logger=test_logger)
    # Test expected object type and handlers
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)
    assert len(test_logger.handlers) == 1  # Only 1 handler
    assert test_logger.handlers[0].name == "SystemConsoleHandler"
    # Test console logger has been set at INFO level (20)
    assert test_logger.handlers[0].level == 20


def test_add_system_console_handler_custom_name():
    """Test add system console handler to a logger - with a custom name."""
    # Create a test logger
    test_logger = logging.getLogger("console_handler_test_custom_name")
    # Add handler to the logger, set test name
    add_system_console_handler(logger=test_logger, handler_name="TestConsoleHandler")
    # Test expected object type and handlers
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.StreamHandler)
    assert len(test_logger.handlers) == 1  # Only 1 handler
    assert test_logger.handlers[0].name == "TestConsoleHandler"
    # Test console logger has been set at INFO level (20)
    assert test_logger.handlers[0].level == 20


def test_add_system_log_file_handler(tmp_path):
    """Test the add_system_log_file_handler function."""
    # Name test log file within the pytest temp path
    test_log_path = tmp_path / "test.log"
    # Get a test logger by name
    test_logger = logging.getLogger("system_log_file_handler_test")
    # Add the log file handler
    add_system_log_file_handler(logger=test_logger, log_path=test_log_path)
    # Test log type, handlers, file existence
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert len(test_logger.handlers) == 1  # Only 1 handler
    assert test_logger.handlers[0].name == "SystemFileHandler"
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    assert test_log_path.is_file()
    # Test file logger has been set at DEBUG level (10)
    assert test_logger.handlers[0].level == 10


# TODO convert to parameterised tests
def test_add_system_log_file_handler_custom_name(tmp_path):
    """Test the add_system_log_file_handler function."""
    # Name test log file within the pytest temp path
    test_log_path = tmp_path / "test.log"
    # Get a test logger by name
    test_logger = logging.getLogger("system_log_file_handler_test_custom")
    # Add the log file handler
    add_system_log_file_handler(
        logger=test_logger, log_path=test_log_path, handler_name="TestFileHandler"
    )
    # Test log type, handlers, file existence
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert len(test_logger.handlers) == 1  # Only 1 handler
    assert test_logger.handlers[0].name == "TestFileHandler"
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    assert test_log_path.is_file()
    # Test file logger has been set at DEBUG level (10)
    assert test_logger.handlers[0].level == 10


# Test side effect - custom name
def side_effect_func_custom(logger, log_path, handler_name=None):
    """Side effect for use in tests only."""
    # Mocks the add_system_log_file_handler function
    # Create log formatter
    file_formatter = logging.Formatter(
        fmt="%(asctime)s : %(name)s : %(levelname)s "
        ": %(message)s : %(filename)s -> %(funcName)s()",
        datefmt="%y-%m-%d %H:%M",
    )
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "TESTFileHandler"
    # Create main system log handler
    file_handler = logging.FileHandler(log_path, mode="a")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set level for log file - debug and above
    file_handler.setLevel(logging.DEBUG)
    # Add content formatter to the logger
    file_handler.setFormatter(file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


# Tests for create_system_logger function
# Different tests required for default logger name at package root, or custom name
def test_create_system_logger_custom_name(tmp_path):
    """Test the create_system_logger function - with custom name."""
    # Create test log file in pytest temp path
    test_log_path = tmp_path / "test.log"
    with patch(
        "simple.logger.log.add_system_log_file_handler",
        side_effect=side_effect_func_custom,
    ):
        # Create system logger with specified name
        test_logger = create_system_logger(
            log_path=test_log_path,
            logger_name="test_logger_custom",
            file_handler_name="TestFileHandler",
        )
        # Test for expected type and presence of handlers
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.hasHandlers()
        assert len(test_logger.handlers) == 1  # Only 1 handler
        # For non default named system logger then only log file handlers will exist
        # No stream handler, because no access to default system logger via init
        assert isinstance(test_logger.handlers[0], logging.FileHandler)
        assert "StreamHandler" not in str(test_logger.handlers)
        # Test log file exists
        assert test_log_path.is_file()
        # Test expected name has been set
        assert test_logger.name == "test_logger_custom"
        # Test handler name
        assert test_logger.handlers[0].name == "TestFileHandler"
        # Test expected logger level has been set DEBUG = 10
        assert test_logger.level == 10
        # Test expected handler level has been set DEBUG = 10
        assert test_logger.handlers[0].level == 10


def side_effect_func(logger, log_path, handler_name=None):
    """Side effect for use in tests only."""
    # Mocks the add_system_log_file_handler function
    # Create log formatter
    file_formatter = logging.Formatter(
        fmt="%(asctime)s : %(name)s : %(levelname)s "
        ": %(message)s : %(filename)s -> %(funcName)s()",
        datefmt="%y-%m-%d %H:%M",
    )
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "TESTFileHandler"
    # Create main system log handler
    file_handler = logging.FileHandler(log_path, mode="a")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set level for log file - debug and above
    file_handler.setLevel(logging.DEBUG)
    # Add content formatter to the logger
    file_handler.setFormatter(file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


# Unit test, so need to mock out intermediate function calls
# create_system_logger uses add_system_log_file_handler
def test_create_system_logger_default_name(tmp_path):
    """Test the create_system_logger function."""
    # Create test log file in pytest temp path
    test_log_path = tmp_path / "test.log"
    with patch(
        "simple.logger.log.add_system_log_file_handler", side_effect=side_effect_func
    ):
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
        # Don't test for number of handlers, system file handler will be added onto
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
        print(handler_names)
