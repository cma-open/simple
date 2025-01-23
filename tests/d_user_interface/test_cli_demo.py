"""UI Tests for the system demos."""

import subprocess
from importlib import import_module
from importlib.metadata import entry_points

# Set demo test constants
DEMO_LOG_FILES = ["demo_config.log", "demo_system.log"]

# See pyproject.toml for full list of system scripts
# cli-demo-logs = "simple.demos.demos:demo_logs_cli_entry_point" (uses argparse)
# demo-logs = "simple.cli:demo_logs_main"

# These tests check these script as if they were run at the command line by a user
# Check script call, user options and expected outputs (inc. log to file or console)
# ----------------------------------------------------------------------
# test_demo_logs_call_user_arg
#    "demo-logs" call with custom dir as tmp_path
# "demo_logs" is not tested without user args as that would write to disk
# also such tests are covered by module tests for the function
# test_entry_points_demo_logs
#    check "demo-logs" command script registered correctly
# ----------------------------------------------------------------------
# test_cli_demo_logs_dry_run
# test "cli-demo-logs" with dry run option
# test_cli_demo_logs_with_user_args
# test "cli-demo-logs" with custom dir as tmp_path
# test_entry_points_cli_demo_logs
#    test "cli-demo-logs" command script registered correctly
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Tests for simple "demo-logs" script function (no use of argparse)
# demo-logs command calls demo_logs_main at simple.cli.demo_logs_main
# main component function simple.demos.demos.demo_logs
# logs occur at - demos.demos.system_logger but disabled if run by pytest
# ----------------------------------------------------------------------


def test_demo_logs_call_user_arg(tmp_path):
    """Test the demo-logs command - with user path argument."""
    # Note - the script name is set via project.scripts in pyproject.toml
    # Note - this is a basic command call to the function, no argparse
    # Note capsys and caplog don't work well with subprocesses
    CLI_CALL = "demo-logs"
    user_path_arg = str(tmp_path)
    # Run the command line call - pass tmp_path as target directory
    out = subprocess.run(
        [CLI_CALL, user_path_arg],
        check=True,
        text=True,
    )  # nosec
    # Reminder - If check is true, and the process exits with a non-zero exit code,
    # a CalledProcessError exception will be raised. Attributes of exception hold
    # the arguments, the exit code, and stdout and stderr if they were captured
    # Confirm success when run with help option
    assert out.returncode == 0
    # Check log files have been saved to test tmp_path
    # Set full path locations x2
    demo_system_log = tmp_path / DEMO_LOG_FILES[1]
    demo_config_log = tmp_path / DEMO_LOG_FILES[0]
    # Check the specific demo logs now exist
    assert demo_config_log.is_file()
    assert demo_system_log.is_file()
    # Check files are not empty
    assert demo_config_log.stat().st_size != 0
    assert demo_system_log.stat().st_size != 0
    # No logs to stdout, output to system.log file (disabled in tests)
    # See other tests under a_unit/demos/


def test_entry_point_demo_logs():
    """Tests to check the command line scripts have been set correctly."""
    # Get current list of installed console scripts
    scripts = entry_points(group="console_scripts")
    # Set name of script being tested
    cli_script = "demo-logs"
    # Check the named script exists in the list of system scripts
    assert cli_script in scripts.names
    # Cast to tuple, as selection for current script under test
    (script,) = entry_points(group="console_scripts", name=cli_script)
    # Get imported parent module by name
    test_module = import_module(script.module)
    # Check the function exists within the parent module
    # This checks demo_logs is callable from the demos module
    assert hasattr(test_module, script.attr)
    # Further check of full path (kept just to illustrate access)
    assert script.value == "simple.cli:demo_logs_main"


# ----------------------------------------------------------------------
# Tests for cli tool function - with argparse
# ----------------------------------------------------------------------


def test_cli_demo_logs_dry_run():
    """Test the command can be called with user args.

    Allows verification that CLI tool is correctly installed.
    """
    CLI_CALL = "cli-demo-logs"
    try:
        out = subprocess.run(  # nosec  # bandit ignore
            [CLI_CALL, "--dry"],
            check=True,
            capture_output=True,
            text=True,
        )  # nosec  # bandit ignore
        # Check if exit code indicates success (0 = success)
        assert out.returncode == 0
    except subprocess.CalledProcessError as error:
        print(error.stdout)
        print(error.stderr)
        raise error


def test_cli_demo_logs_with_user_args(tmp_path):
    """Test the command can be called with user args.

    Allows verification that CLI tool is correctly installed.
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


def test_entry_point_cli_demo_logs():
    """Tests to check the command line scripts have been set correctly."""
    # Get current list of installed console scripts
    scripts = entry_points(group="console_scripts")
    # Set name of script being tested
    cli_script = "cli-demo-logs"
    # Check the named script exists in the list of system scripts
    assert cli_script in scripts.names
    # Cast to tuple, as selection for script under test
    (script,) = entry_points(group="console_scripts", name=cli_script)
    # Get imported parent module by name
    test_module = import_module(script.module)
    # Check the function exists within the parent module
    # e.g. this checks demo_logs is callable from the demos module
    assert hasattr(test_module, script.attr)
    # Further check of full path (kept just to illustrate access)
    assert script.value == "simple.cli:demo_logs_cli_entry_point"
