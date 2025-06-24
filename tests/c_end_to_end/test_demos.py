"""End to end tests for the system demos."""

# End to end test notes
# Aim to test software from start to finish (as used by the user)
# If testing API, then make calls as clients would.

# Dev notes
# At this stage some of these test are effectively duplicates of other tests
# More realistic tests will be added as the system evolves

import subprocess

# Set demo test constants
DEMO_LOG_FILES = ["demo_config.log", "demo_system.log"]


def test_cli_demo_logs_with_user_args(tmp_path):
    """Test the command can be called with user args.

    Shows end to end run that demo logs are created.
    """
    CLI_CALL = "cli-demo-logs"
    demo_log_dir = tmp_path
    out = subprocess.run(  # nosec  # bandit ignore
        [CLI_CALL, demo_log_dir],
        check=True,
        capture_output=True,
        text=True,
    )  # nosec  # bandit ignore
    # Check if exit code indicates success (0 = success)
    assert out.returncode == 0
    # Confirm log files were created within temp_path
    # Set full path location for demo_temp log files x2
    demo_system_log = tmp_path / DEMO_LOG_FILES[1]
    demo_config_log = tmp_path / DEMO_LOG_FILES[0]
    # Check logs now exist
    assert demo_config_log.is_file()
    assert demo_system_log.is_file()
    # Check files are not empty
    assert demo_config_log.stat().st_size != 0
    assert demo_system_log.stat().st_size != 0
