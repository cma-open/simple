"""Unit tests for the demos module."""

import logging
import re
from unittest.mock import patch

from simple.demos.demos import demo_config_file_log, demo_system_console_log

# Set test module constants
# Set expected logger names
DEMO_CONFIG_LOGGER_NAME = "DemoConfigLog"
DEMO_SYSTEM_LOGGER_NAME = "DemoSystemLog"

# --------------------------------------------------------------------------------------
# Test for log outputs from demo_temp functions
# --------------------------------------------------------------------------------------


def config_side_effect_func(log_path, logger_name):
    """Side effect for use in tests only."""
    # Set features to mimic create_config_logger and add_config_log_file_handler
    config_file_formatter = logging.Formatter(
        fmt="%(asctime)s %(message)s",
        datefmt="%y-%m-%d %H:%M",
    )
    if logger_name is None:
        logger_name = DEMO_CONFIG_LOGGER_NAME
    test_logger = logging.getLogger(logger_name)
    # Set logging level - logger level
    test_logger.setLevel(logging.DEBUG)
    # Set default handler name if no argument supplied
    handler_name = "DemoConfigFileHandler"
    file_handler = logging.FileHandler(log_path, mode="w")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set logging level - handler level
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(config_file_formatter)
    # Add handler to the logger
    test_logger.addHandler(file_handler)
    return test_logger


# demo_config_file itself calls create_config_logger
# therefore this needs to be mocked out
def test_demo_config_file_log_no_console(tmp_path, capsys):
    """Test the demo_config_logger function."""
    # Unit test so requires controlling function subcalls
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    with patch(
        "simple.demos.demos.create_config_logger", side_effect=config_side_effect_func
    ):
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
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    with patch(
        "simple.demos.demos.create_config_logger", side_effect=config_side_effect_func
    ):
        # Run the demo_temp logger - Write file into tmp_path
        demo_config_file_log(test_log_file)
        # Test log message is as expected
        assert "Config demo_temp started" in caplog.text
        assert "Config demo_temp" in caplog.text
        assert "Config demo_temp finished" in caplog.text
        assert len(caplog.records) == 3
        # Test log name is as expected
        assert caplog.records[0].name == "DemoConfigLog"


def test_demo_config_file_log_file_content(tmp_path):
    """Test the demo_config_logger function."""
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    with patch(
        "simple.demos.demos.create_config_logger", side_effect=config_side_effect_func
    ):
        # Run the demo_temp logger - Write file into tmp_path
        demo_config_file_log(test_log_file)
        # Test content of log file
        with open(test_log_file, "r") as test_log:
            content = test_log.readlines()
            # print(content)
            # Expect 3 lines of log message
            assert len(content) == 3
            # Simple test that file content holds ex[ect string
            assert "Config demo_temp started" in content[0]
            assert "Config demo_temp" in content[1]
            assert "Config demo_temp finished" in content[2]
            # Set search pattern for the expected time format
            search_pattern = "[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"
            # Test file content is as expected, including time format
            assert re.match(f"{search_pattern} Config demo_temp started", content[0])
            assert re.match(f"{search_pattern} Config demo_temp", content[1])
            assert re.match(f"{search_pattern} Config demo_temp finished", content[2])
            # Note test is verbose and duplicated for training use


# ----------
# System log
# ----------


# create side effect for use in tests
# mimics create_system_logger
def side_effect_func(log_path, logger_name, file_handler_name=None):
    """Side effect for use in tests only."""
    # Mocks the create_system_logger function
    # Will require updates if any changes to components
    # covers: file_formatter, create logger and set level
    # add system log file handler
    # Create log formatter
    file_formatter = logging.Formatter(
        fmt="%(asctime)s : %(name)s : %(levelname)s "
        ": %(message)s : %(filename)s -> %(funcName)s()",
        datefmt="%y-%m-%d %H:%M",
    )
    # Set default logger name
    logger_name = DEMO_SYSTEM_LOGGER_NAME
    # Get logger name from argument or default
    logger = logging.getLogger(logger_name)
    # Set initial level for the logger
    logger.setLevel(logging.DEBUG)
    # Add handlers to the logger
    # info level and above goes to console (already set by init)
    # debug level and above go to file
    # Set default handler name if no argument supplied
    handler_name = "DemoSystemFileHandler"
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


# unit test so need to mock out intermediate calls
# create_system_logger
def test_demo_system_console_log(tmp_path, caplog, capsys):
    """Test the demo_system_console_log function."""
    log_file = tmp_path / "test.log"
    # create_system_logger(log_path=log_path, logger_name=DEMO_SYSTEM_LOGGER_NAME,
    #                     file_handler_name=file_handler_name)
    with patch(
        "simple.demos.demos.create_system_logger",
        side_effect=side_effect_func,
    ):
        # Run the demo log (logs to both file and to console)
        test_logger = demo_system_console_log(log_file)
        # Test expected log level has been set DEBUG = 10
        assert test_logger.level == 10
        # test expected logger name
        assert test_logger.name == DEMO_SYSTEM_LOGGER_NAME
        # Test output to log file - as captured by caplog
        # Expect both .info and .debug level to log to file
        assert "System demo_temp started" in caplog.text  # .debug level
        assert "System demo_temp" in caplog.text  # .info level
        assert "System demo_temp finished" in caplog.text  # .debug level
        # Test for expected number of log records in log file
        assert len(caplog.records) == 3
        # Test logger name, as captured by each record
        assert caplog.records[0].name == DEMO_SYSTEM_LOGGER_NAME
        # Collect the current handler names
        handler_names = [handler.name for handler in test_logger.handlers]
        print(handler_names)

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


# def test_demo_system_console_log_console(tmp_path, capsys):
#     """Test the demo_system_console_log function."""
#     log_file = tmp_path / "test.log"
#     # Run the demo log (logs to both file and to console)
#     demo_system_console_log(log_file)
#
#     # Test output to console - as captured by capsys
#     # Expect only .info level and above to console
#     # Capture console output during test
#     captured = capsys.readouterr()
#
#     print("-")
#     print(captured)
#     print("-")
#     # Only expect one line of output to console
#     expected = "DEMOLog                     : INFO    : System demo_temp\n"
#     # Test that only some output to console
#     assert captured.out == expected
