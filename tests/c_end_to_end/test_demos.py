"""End to end tests for the system demos."""

# End to end test notes
# Aim to test software from start to finish (as used by the user)
# If testing API, then make calls as clients would.

from simple.definitions import DEMO_TEMP_DIR
from simple.demos.demos import demo_logs


def test_demo_system_log():
    """Test the demo_temp for the system log."""
    # Tests may run in situation where directory exists or does not exist
    # Therefore deal with both cases
    # If directory already exists then empty it
    # Testing actual data directories (not just within temp dir)
    if DEMO_TEMP_DIR.is_dir():
        # Remove any existing demo_temp log files
        demo_files = list(DEMO_TEMP_DIR.iterdir())
        for demo_file in demo_files:
            demo_file.unlink(missing_ok=True)
        # Confirm the directory was emptied
        assert any(DEMO_TEMP_DIR.iterdir()) is False

    # Run the demo function
    demo_logs()
    # Get expected output log names
    test_config_log_file = DEMO_TEMP_DIR / "demo_config.log"
    test_system_log_file = DEMO_TEMP_DIR / "demo_system.log"
    # Test log files were created
    assert test_config_log_file.is_file()
    assert test_system_log_file.is_file()

    # TODO check later
    # Check console log output is as expected
    # expected = (
    #    "DEMOLog :: INFO     :: System demo_temp                   \n"
    #    "DEMOLog :: WARNING  :: System warning                     \n"
    # )
    # assert output.stderr == expected

    # TODO - tidy up / delete
    # Create dir if it does not yet exist
    # DEMO_TEMP_DIR.mkdir(exist_ok=True)
    # Set the path to the logger module
    # log_main = str(PACKAGE_DIR / "logger" / "log.py")
    # Run the logger module to run the demos
    # output = subprocess.run(  # nosec
    #    ["python", log_main], capture_output=True, text=True
    # )  # nosec
    # Get expected output log names
    # test_config_log_file = DEMO_TEMP_DIR / "demo_config.log"
    # test_system_log_file = DEMO_TEMP_DIR / "demo_system.log"
    # Test log files were created
    # assert test_config_log_file.is_file()
    # assert test_system_log_file.is_file()
    # Check console log output is as expected
    # expected = (
    #    "SystemLog :: INFO     :: System demo_temp                   \n"
    #    "SystemLog :: WARNING  :: System warning                     \n"
    # )
    # assert output.stderr == expected

    # TODO expand tests to also read log file content on disk
    # TODO double check any option to mock out demo_temp dir
    #  e.g. via subprocess, not possible?
