"""UI Tests for the system demos."""

import logging
import subprocess
from importlib import import_module
from importlib.metadata import entry_points

from simple.common.common import clean_directory
from simple.config.reader import return_datadir

system_logger = logging.getLogger(__name__)

# Set demo test constants
DEMO_TEMP_DIR = return_datadir() / "demo_temp"
DEMO_LOG_FILES = ["demo_config.log", "demo_system.log"]

# ----------------------------------------------------------------------
# Tests for simple script function (no use of argparse)
# ----------------------------------------------------------------------


def test_demo_logs_call():
    """Test the demo-logs command."""
    # Note - the script name is set via project.scripts in pyproject.toml
    # Note - this is a basic command call to the function, no argparse
    # Note - WARNING -currently this test modifies actual content on disk
    # Ensure demo_temp is empty
    clean_directory(dir_path=DEMO_TEMP_DIR, files=DEMO_LOG_FILES)
    CLI_CALL = "demo-logs"
    # Run the command line call
    out = subprocess.run([CLI_CALL], check=True)  # nosec
    # Reminder - If check is true, and the process exits with a non-zero exit code,
    # a CalledProcessError exception will be raised. Attributes of exception hold
    # the arguments, the exit code, and stdout and stderr if they were captured
    # Confirm success when run with help option
    assert out.returncode == 0
    # Check log files have been saved to expected locations
    # Issues here are
    #   - overwriting already in-use locations
    #   - not possible to mock command calls via subprocess?
    # Set full path location for demo_temp log files x2
    demo_system_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[1]
    demo_config_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[0]
    # Check logs now exist
    assert demo_config_log.is_file()
    assert demo_system_log.is_file()
    # Check files are not empty
    assert demo_config_log.stat().st_size != 0
    assert demo_system_log.stat().st_size != 0


def test_entry_point_demo_logs():
    """Tests to check the command line scripts have been set correctly."""
    # Get current list of installed console scripts
    scripts = entry_points(group="console_scripts")
    # Set name of script being tested
    cli_script = "demo-logs"
    # Check the named script exists
    assert cli_script in scripts.names
    # Cast to tuple, as selection for script under test
    (script,) = entry_points(group="console_scripts", name=cli_script)
    # Get imported parent module by name
    test_module = import_module(script.module)
    # Check the function exists within the parent module
    # e.g. this checks demo_logs is callable from the demos module
    assert hasattr(test_module, script.attr)
    # Further check of full path (kept just to illustrate access)
    assert script.value == "simple.demos.demos:demo_logs"


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
