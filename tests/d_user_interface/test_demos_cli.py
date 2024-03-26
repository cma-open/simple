"""UI Tests for the system demos."""

import logging
import subprocess

from simple.common.common import clean_directory
from simple.config.reader import return_datadir

system_logger = logging.getLogger(__name__)

# Set demo test constants
DEMO_TEMP_DIR = return_datadir() / "demo_temp"
DEMO_LOG_FILES = ["demo_config.log", "demo_system.log"]


def test_demo_logs_cli_call():
    """Test the demo-logs command."""
    # Note - the script name is set via project.scripts in pyproject.toml
    # Note - this is a basic command call top the function, no argparse
    # Note - currently this test modifies actual content on disk

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
    #   - not possible to mock command calls via subprocess

    # Set full path location for demo_temp log files x2
    demo_system_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[1]
    demo_config_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[0]

    # Check logs now exist
    assert demo_config_log.is_file()
    assert demo_system_log.is_file()
    # Check files are not empty
    assert demo_config_log.stat().st_size != 0
    assert demo_system_log.stat().st_size != 0
