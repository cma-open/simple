"""Unit tests for the log module - config logger."""

import logging
from unittest.mock import patch

from simple.logger.log import add_config_log_file_handler, create_config_logger


def test_add_config_log_file_handler(tmp_path):
    """Test the add_config_log_file_handler function."""
    test_log_path = tmp_path / "test.log"
    test_logger = logging.getLogger("config_log_file_handler_test")
    add_config_log_file_handler(logger=test_logger, log_path=test_log_path)
    # Confirm main logger properties as expected
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert test_log_path.is_file()
    # Confirm handler properties
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    # Test handlers have the expected log levels set
    assert [
        handler.level == 10
        for handler in test_logger.handlers
        if handler.name == "ConfigFileHandler"
    ]


# Mock out the intermediate call to add config log handler


def side_effect_func(logger, log_path, handler_name=None):
    """Side effect for use in tests only."""
    config_file_formatter = logging.Formatter(
        fmt="%(asctime)s %(message)s",
        datefmt="%y-%m-%d %H:%M",
    )
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "TESTConfigFileHandler"
    file_handler = logging.FileHandler(log_path, mode="w")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set logging level
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(config_file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


def test_create_config_logger(tmp_path):
    """Test the create_config_logger function."""
    test_log_path = tmp_path / "test.log"
    with patch(
        "simple.logger.log.add_config_log_file_handler", side_effect=side_effect_func
    ):
        # Create system logger
        # As a default this will use package log name
        # Therefore this will access default system logger created via init
        test_logger = create_config_logger(log_path=test_log_path)
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.hasHandlers()
        assert "FileHandler" in str(test_logger.handlers[0])
        assert test_log_path.is_file()
        # No stream handler, because  no access to default system logger via init
        assert isinstance(test_logger.handlers[0], logging.FileHandler)
        assert "StreamHandler" not in str(test_logger.handlers)
        # Test log file exists
        assert test_log_path.is_file()
        # Test expected name has been set
        assert test_logger.name == "ConfigLog"
        # Test handler name
        assert test_logger.handlers[0].name == "ConfigFileHandler"
        # Test expected logger level has been set DEBUG = 10
        assert test_logger.level == 10
        # Test expected handler level has been set DEBUG = 10
        assert test_logger.handlers[0].level == 10


def test_create_config_logger_custom_name(tmp_path):
    """Test the create_config_logger function."""
    test_log_path = tmp_path / "test.log"
    with patch(
        "simple.logger.log.add_config_log_file_handler", side_effect=side_effect_func
    ):
        # Create system logger
        # As a default this will use package log name
        # Therefore this will access default system logger created via init
        test_logger = create_config_logger(
            log_path=test_log_path, logger_name="TestConfigLog"
        )
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.hasHandlers()
        assert "FileHandler" in str(test_logger.handlers[0])
        assert test_log_path.is_file()
        # No stream handler, because no access to default system logger via init
        assert isinstance(test_logger.handlers[0], logging.FileHandler)
        assert "StreamHandler" not in str(test_logger.handlers)
        # Test log file exists
        assert test_log_path.is_file()
        # Test expected name has been set
        assert test_logger.name == "TestConfigLog"
        # Test handler name
        assert test_logger.handlers[0].name == "TESTConfigFileHandler"
        # Test expected logger level has been set DEBUG = 10
        assert test_logger.level == 10
        # Test expected handler level has been set DEBUG = 10
        assert test_logger.handlers[0].level == 10
