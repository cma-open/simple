"""Unit tests for the demo module."""

from simple.demos.demos import demo_config_file_log, demo_system_console_log


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
    assert "System demo_temp finished" in caplog.text
    # Test expected number of log records
    assert len(caplog.records) == 3
    # Test log name. Set to DEMOLog for these logs
    assert caplog.records[0].name == "DEMOLog"
    # Capture the output to console
    captured = capsys.readouterr()
    # Set expected output
    expected = "DEMOLog                     : INFO    : System demo_temp\n"
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
    # Test that there is no output to the console
    # ConfigLog is expected to be to file only
    assert captured.err == ""
