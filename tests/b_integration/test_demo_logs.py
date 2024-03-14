"""Integration tests for the demos module."""

import re

from simple.demos.demos import demo_config_file_log

# demo_system_console_log

# --------------------------------------------------------------------------------------
# Test for log outputs from demo_temp functions
# --------------------------------------------------------------------------------------


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
    # Test log name is as expected
    assert caplog.records[0].name == "DemoConfigLog"


def test_demo_config_file_log_file_content(tmp_path):
    """Test the demo_config_logger function."""
    # Context / reminder
    # func creates named logger with file handler and DEBUG level
    # no console handler is used
    test_log_file = tmp_path / "test.log"
    # Run the demo_temp logger - Write file into tmp_path
    demo_config_file_log(test_log_file)
    # Test content of log file
    with open(test_log_file, "r") as test_log:
        content = test_log.readlines()
        print(content)
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


# def test_demo_config_file_log(tmp_path, caplog, capsys):
#     """Test the demo_config_logger function."""
#     # Context / reminder
#     # func creates named logger with file handler and DEBUG level
#     # no console handler is used
#     test_log_file = tmp_path / "test.log"
#     # Run the demo_temp logger - Write file into tmp_path
#     demo_config_file_log(test_log_file)
#     # Test file was created
#     assert test_log_file.is_file()
#
#     # Test log message is as expected
#     assert "Config demo_temp started" in caplog.text
#     assert "Config demo_temp" in caplog.text
#     assert "Config demo_temp finished" in caplog.text
#     assert len(caplog.records) == 3
#     # Test log name is as expected
#     assert caplog.records[0].name == "ConfigLog"
#     # Capture the output to console
#     captured = capsys.readouterr()
#     # Test that there is no output to the console
#     # ConfigLog is expected to be to file only
#     assert captured.err == ""
#


# def test_demo_system_console_log(tmp_path, caplog, capsys):
#     """Test the demo_system_console_log function."""
#     log_file = tmp_path / "test.log"
#     # Run the demo log (logs to both file and to console)
#     demo_system_console_log(log_file)
#
#     # Test output to log file - as captured by caplog
#     # Expect both .info and .debug level to log to file
#     assert "System demo_temp started" in caplog.text  # .debug level
#     assert "System demo_temp" in caplog.text # .info level
#     assert "System demo_temp finished" in caplog.text  # .debug level
#     # Test for expected number of log records in log file
#     assert len(caplog.records) == 3
#     # Test log name.
#     # Name was set to DEMOLog for these logs
#     assert caplog.records[0].name == "DEMOLog"
#     caplog.clear()
#     # Test output to console - as captured by capsys
#     # Expect only .info level and above to console
#     # Capture console output during test
#     captured = capsys.readouterr()
#     demo_system_console_log(log_file)
#
#     print(caplog.records)
#     print(caplog.record_tuples)
#     captured = capsys.readouterr()
#     print("-")
#     print(captured)
#     print("-")
#     # Only expect one line of output to console
#     expected = "DEMOLog                     : INFO    : System demo_temp\n"
#     # Test that only some output to console
#     assert captured.out == expected

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
