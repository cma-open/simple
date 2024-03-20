"""Integration tests for the demos module."""

import re

from simple.demos.demos import demo_config_file_log, demo_logs, demo_system_console_log

# --------------------------------------------------------------------------------------
# Test for log outputs from demo_temp functions
# --------------------------------------------------------------------------------------

# Set test module constants
# Set expected logger names
CONFIG_LOGGER_NAME = "DemoConfigLog"
SYSTEM_LOGGER_NAME = "DemoSystemLog"

# ----------
# Config log
# ----------


def test_demo_config_file_log_no_console(tmp_path, capsys):
    """Test the demo_config_logger function."""
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    # Run the demo_temp logger - Write file into tmp_path
    demo_config_file_log(test_log_file)
    # Test file was created
    assert test_log_file.is_file()
    # Capture the output to console
    captured = capsys.readouterr()
    # Test that there is no output to the console
    # ConfigLog is expected to be to file only
    assert captured.err == ""
    assert captured.out == ""


def test_demo_config_file_log_output(tmp_path, caplog):
    """Test the demo_config_logger function."""
    # Test - shows use of caplog
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    # Run the demo_temp logger - Write file into tmp_path
    demo_config_file_log(test_log_file)
    # Test log message is as expected
    assert "Config demo_temp started" in caplog.text
    assert "Config demo_temp" in caplog.text
    assert "Config demo_temp finished" in caplog.text
    assert len(caplog.records) == 3
    # Test logger name is as expected
    assert caplog.records[0].name == CONFIG_LOGGER_NAME


def test_demo_config_file_log_file_content(tmp_path):
    """Test the demo_config_logger function."""
    # Test - uses direct read of file within tmp_path (not caplog)
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    # Run the demo_temp logger - Write file into tmp_path
    demo_config_file_log(test_log_file)
    # Test content of log file
    with open(test_log_file, "r") as test_log:
        # Read file content
        content = test_log.readlines()
        # Expect 3 lines of log message
        assert len(content) == 3
        # Simple test that file content holds expected string
        # Note this does not test expected timestamp
        assert "Config demo_temp started" in content[0]
        assert "Config demo_temp" in content[1]
        assert "Config demo_temp finished" in content[2]
        # Set search pattern for the expected time format
        # Example format 24-03-19 15:37 Config demo_temp started
        search_pattern = "[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"
        # Test file content is as expected, including time format
        assert re.match(f"{search_pattern} Config demo_temp started", content[0])
        assert re.match(f"{search_pattern} Config demo_temp", content[1])
        assert re.match(f"{search_pattern} Config demo_temp finished", content[2])
        # Note test is verbose and duplicated for training use


# ----------
# System log
# ----------


def test_demo_system_console_log(tmp_path, caplog, capsys):
    """Test the demo_system_console_log function."""
    log_file = tmp_path / "test.log"
    # Run the demo log (logs to both file and to console)
    test_logger = demo_system_console_log(log_file)
    # Test expected log level has been set DEBUG = 10
    assert test_logger.level == 10
    # test expected logger name
    assert test_logger.name == SYSTEM_LOGGER_NAME
    # Test output to log file - as captured by caplog
    # Expect both .info and .debug level to log to file
    assert "System demo_temp started" in caplog.text  # .debug level
    assert "System demo_temp" in caplog.text  # .info level
    assert "System demo_temp finished" in caplog.text  # .debug level
    # Test for expected number of log records in log file
    assert len(caplog.records) == 3
    # Test logger name, as captured by each record
    assert caplog.records[0].name == SYSTEM_LOGGER_NAME
    # Test expected handler names
    assert test_logger.hasHandlers()
    assert test_logger.handlers[0].name == "DemoSystemConsoleHandler"
    assert test_logger.handlers[1].name == "DemoSystemFileHandler"
    # Test handlers have the expected log levels set
    assert [
        handler.level == 20
        for handler in test_logger.handlers
        if handler.name == "DemoSystemConsoleHandler"
    ]
    assert [
        handler.level == 10
        for handler in test_logger.handlers
        if handler.name == "DemoSystemFileHandler"
    ]
    # Confirm that only one record - info level - was output to terminal
    captured = capsys.readouterr()
    # Only expect one line of output to console
    expected = "DemoSystemLog               : INFO    : System demo_temp\n"
    # Test that only some output to console
    assert captured.err == expected


# ----------
# demo logs
# ----------


def test_demo_logs(tmp_path):
    """Test the demo_logs function."""
    demo_logs(demo_temp_dir=tmp_path)
    demo_system_log = tmp_path / "demo_system.log"
    demo_config_log = tmp_path / "demo_config.log"
    # Test files have been created
    assert demo_system_log.is_file()
    assert demo_config_log.is_file()
    # Test system log content
