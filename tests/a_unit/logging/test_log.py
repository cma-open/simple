"""Unit tests for the log module."""

import logging

from simple.logging.log import (
    add_system_console_handler,
    add_system_log_file_handler,
    create_config_logger,
    create_system_logger,
    demo_config_file_log,
    demo_system_console_log,
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


def test_add_config_log_file_handler(tmp_path):
    """Test the add_config_log_file_handler function."""
    test_log_path = tmp_path / "test.log"
    test_logger = logging.getLogger("config_log_file_handler_test")
    add_system_log_file_handler(logger=test_logger, log_path=test_log_path)

    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert isinstance(test_logger.handlers[0], logging.FileHandler)
    print(test_logger.handlers)
    assert test_log_path.is_file()


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


def test_create_config_logger(tmp_path):
    """Test the create_config_logger function."""
    test_log_path = tmp_path / "test.log"
    test_logger = create_config_logger(log_path=test_log_path)
    test_logger.info("test")
    assert isinstance(test_logger, logging.Logger)
    assert test_logger.hasHandlers()
    assert "FileHandler" in str(test_logger.handlers[0])
    assert test_log_path.is_file()


# --------------------------------------------------------------------------------------
# Test for log outputs from demo_temp functions
# --------------------------------------------------------------------------------------
def test_demo_system_logger(tmp_path, caplog, capsys):
    """Test the demo_system_logger function."""
    log_file = tmp_path / "test.log"
    demo_system_console_log(log_file)
    # Test log message is as expected (captured log, as written to file)
    assert "System demo_temp started" in caplog.text
    assert "System demo_temp" in caplog.text
    assert "System warning" in caplog.text
    assert "System demo_temp finished" in caplog.text
    # Test expected number of log records
    assert len(caplog.records) == 4
    # Test log name
    assert caplog.records[0].name == "SystemLog"
    # Capture the output to console
    captured = capsys.readouterr()
    # Set expected output
    expected = (
        "SystemLog :: INFO     :: System demo_temp                   \n"
        "SystemLog :: WARNING  :: System warning                     \n"
    )
    # Test that only some output to console
    assert captured.err == expected


def test_demo_config_logger(tmp_path, caplog, capsys):
    """Test the demo_config_logger function."""
    test_log_file = tmp_path / "test.log"
    # Run the demo_temp logger
    demo_config_file_log(test_log_file)
    # Test file was created
    assert test_log_file.is_file()

    # Test log message is as expected
    assert "Config demo_temp started" in caplog.text
    assert "Config demo_temp" in caplog.text
    assert "Config demo_temp finished" in caplog.text
    assert len(caplog.records) == 3
    # Test log name is as expected
    assert caplog.records[0].name == "ConfigLog"
    # Capture the output to console
    captured = capsys.readouterr()
    # Test that there is no ouput to the console
    # ConfigLog is expected to be to file only
    assert captured.err == ""
