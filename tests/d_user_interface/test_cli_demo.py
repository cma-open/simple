"""UI Tests for the system demos."""

import logging
import os
import subprocess
from importlib import import_module
from importlib.metadata import entry_points
from unittest import mock

from simple.config.reader import return_datadir

system_logger = logging.getLogger(__name__)

# Set demo test constants
DEMO_TEMP_DIR = return_datadir() / "demo_temp"
DEMO_LOG_FILES = ["demo_config.log", "demo_system.log"]

# Set the environment variable to indicate test mode
os.environ["TEST_MODE"] = "1"

# See pyproject.toml for lis of system scripts
# cli-demo-logs = "simple.demos.demos:demo_logs_cli_entry_point" (uses argparse)
# demo-logs = "simple.demos.demos:demo_logs"

# ----------------------------------------------------------------------
# Tests for simple script function (no use of argparse)
# ----------------------------------------------------------------------


# @pytest.fixture(autouse=True)
# def disable_logging():
#    logging.disable(logging.CRITICAL)
#    yield
#    logging.disable(logging.NOTSET)


def test_demo_logs_call(tmp_path):
    """Test the demo-logs command."""
    # Note - the script name is set via project.scripts in pyproject.toml
    # Note - this is a basic command call to the function, no argparse
    # Note capsys and caplog don't work well with subprocesses
    # mock_logger = mocker.patch("simple.demos.demos.system_logger")

    CLI_CALL = "demo-logs"
    # Run the command line call - pass tmp_path as target directory
    out = subprocess.run(
        [CLI_CALL, str(tmp_path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )  # nosec
    # out = subprocess.run([CLI_CALL, str(tmp_path)], check=True, text=True)  # nosec
    # Reminder - If check is true, and the process exits with a non-zero exit code,
    # a CalledProcessError exception will be raised. Attributes of exception hold
    # the arguments, the exit code, and stdout and stderr if they were captured
    # Confirm success when run with help option
    assert out.returncode == 0

    # mock_logger.debug.assert_called_with(
    #    "Running cli-demo-logs tool with:
    #    Namespace(demo_log_dir='test_dir', dry=False)"
    # )
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
    # Check the expected main system log messages occurred
    # assert "Demo logs has run - see files in " in out.stderr
    # print(out.stderr)
    print("Files in tmp_path:")
    for file in tmp_path.iterdir():
        print(file)
    # See other tests under a_unit/demos/


# def test_demo_logs_call_2(tmp_path):
#     """Test the demo-logs command."""
#     # Note - the script name is set via project.scripts in pyproject.toml
#     # Note - this is a basic command call to the function, no argparse
#     # Note capsys and caplog dont work with subprocesses
#     # WARNING -currently this test modifies actual content on disk
#     CLI_CALL = "demo-logs"
#     with patch("simple.demos.demos.DEMO_TEMP_DIR", tmp_path):
#         # Mock the demo_logs function
#         with patch("simple.demos.demos.demo_logs") as mock_demo_logs:
#             # Run the command line call
#             out = subprocess.run(
#                 [CLI_CALL],
#                 check=True,
#                 stdout=subprocess.PIPE,
#             )
#             # Reminder - If check is true, and the process exits with a non-zero code,
#             #                        stderr=subprocess.PIPE, text=True
#             # a CalledProcessError exception is be raised.
#             # Attributes of exception hold
#             # the args, exit code, and stdout and stderr if they were captured
#             # Confirm success when run with help option
#             assert out.returncode == 0
#             # Check log files have been saved to expected locations
#             # Issues here are
#             #   - overwriting already in-use locations
#             #   - not possible to mock command calls via subprocess?
#             # Set full path location for demo_temp log files x2
#             demo_system_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[1]
#             demo_config_log = DEMO_TEMP_DIR / DEMO_LOG_FILES[0]
#             # Check logs now exist
#             assert demo_config_log.is_file()
#             assert demo_system_log.is_file()
#             # Check files are not empty
#             assert demo_config_log.stat().st_size != 0
#             assert demo_system_log.stat().st_size != 0
#             # Check the expected main system log messages occurred
#             assert "Demo logs has run - see files in " in out.stderr
#             # assert mock_demo_logs.assert_called_once_with(#logs)
#             # Print out the files in tmp_path for debugging purposes
#             print("Files in tmp_path:")
#             for file in tmp_path.iterdir():
#                 print(file)


def test_demo_logs_call_mock(tmp_path, mocker, caplog):
    """Test the demo-logs command, capture logs."""
    # Note - the script name is set via project.scripts in pyproject.toml
    # Note - this is a basic command call to the function, no argparse
    # Mock DEMO_TEMP_DIR to be tmp_path
    mocker.patch("simple.demos.demos.DEMO_TEMP_DIR", tmp_path)
    # Mock the subprocess.run call
    # mocker.patch('subprocess.run', return_value=mock.Mock(returncode=0))
    mocker.patch("subprocess.run", side_effect=[mock.Mock(returncode=0)])
    # Ensure the logger is configured to capture INFO level messages
    logger = logging.getLogger("simple.demos.demos")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

    CLI_CALL = "demo-logs"
    with caplog.at_level(logging.INFO):
        # Run the command line call
        out = subprocess.run(
            [CLI_CALL], check=True, capture_output=True, text=True
        )  # nosec
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
        # Verify logger message
        # log_messages = [record.message for record in caplog.records]
        # assert any("Demo logs has run - see files in"
        # in message for message in log_messages)
        print(caplog.text)

        # Print out all captured log messages for debugging purposes
        print("Captured log messages:")
        print(caplog)
        print(caplog.records)
        for record in caplog.records:
            print(record.message)

        # Print captured stderr for debugging purposes
        print("Captured stderr:")
        print(out.stderr)

        assert "Demo logs has run - see files in" in out.stderr

        # Print out the files in tmp_path for debugging purposes
        print("Files in tmp_path:")
        for file in tmp_path.iterdir():
            print(file)


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

    # TODO add more tests with other user defined options
