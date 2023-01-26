"""Test the cli tool."""

# This module uses subprocess, which can raise security threats.
# The risk have been reviewed via Codacy, Bandit.
# The generic warning on import has been left active, in case of future edits here.
# Each specific use warning has been checked and then ignored, where safe to do so.
# bandit ignore command is # nosec, per line

import subprocess  # nosec  # bandit ignore
from pathlib import Path

import pytest

from simple.cli import cli_entry_point
from simple.definitions import PACKAGE_DIR

DEBUG = True

# Define cli filepath
CLI = Path(PACKAGE_DIR, "cli.py")
# No docstring for CLI, to avoid publishing system filepaths
MODULE = "simple.cli"
"""str: Module name."""
TOOL = "cli-simple"
"""str: Script command name."""

# Testing note
# cli tool is registered via entry points in setup.py
# can't be called and run via filepath (does not use main)
# can't be called and run via module name (does not use main)


def test_cli():
    """Test the command can be called via help and version.

    Allows verification that CLI tool is correctly installed (via setup.py)
    """
    # Note - the script tool name is set in the entry_points section of setup.py
    # TODO add a documentation cross ref here
    out = subprocess.run([TOOL, "--help"], check=True)  # nosec
    assert out.returncode == 0

    out = subprocess.run([TOOL, "--version"], check=True)  # nosec
    assert out.returncode == 0


def test_cli_with_user_args():
    """Test the command can be called with user args.

    Allows verification that CLI tool is correctly installed (via setup.py)
    """
    out = subprocess.run(  # nosec  # bandit ignore
        [
            TOOL,
            "1",
            "2",
        ],
        check=True,
        capture_output=True,
        text=True,
    )  # nosec  # bandit ignore
    if DEBUG:
        # print to show CompletedProcess object and args, stdout, stderr, etc
        print(out)
    # Check if exit code indicates success (0 = success)
    assert out.returncode == 0
    # Check the returned command line tool output is as expected
    result = out.stdout.strip()  # remove newline from tool output stdout
    expected = "['3.000005', '3.000005']"
    assert result == expected


def test_cli_with_user_args_raises_errors():
    """Test the command raises errors with incorrect user args."""
    with pytest.raises(subprocess.CalledProcessError):
        # x value too large, expected to cause error
        subprocess.run(  # nosec  # bandit ignore
            [
                TOOL,
                "1000",
                "2",
            ],
            check=True,
            capture_output=True,
            text=True,
        )  # nosec  # bandit ignore


def test_cli_with_user_args_raises_errors_message():
    """Test the command raises errors with incorrect user args."""
    # x value too large, expected to cause error
    out = subprocess.run(  # nosec  # bandit ignore
        [
            TOOL,
            "1000",
            "2",
        ],
        check=False,
        capture_output=True,
        text=True,
    )  # nosec  # bandit ignore
    # note check=False to prevent error code
    print(out.stderr)
    message = out.stderr
    expected = (
        "CLI-SIMPLE: error: argument x: invalid choice: 1000 "
        "(choose from 0, 1, 2, 3, 4, 5)"
    )
    assert expected in message


def test_cli_entry_point_user_input_errors():
    """Test for cli tool user input values."""
    # Create a range of possible user input test arguments
    x_value_too_large = ["--x", "1000000000", "--y", "2"]
    y_value_too_small = ["--x", "2", "--y", "-2"]
    y_argument_missing = ["--x", "1"]
    too_many_arguments = ["--x", "4", "--y", "2", "--z", "3"]

    # Confirm expected errors - expect to fail
    with pytest.raises(SystemExit):
        cli_entry_point(x_value_too_large)
    with pytest.raises(SystemExit):
        cli_entry_point(y_value_too_small)
    with pytest.raises(SystemExit):
        cli_entry_point(y_argument_missing)
    with pytest.raises(SystemExit):
        cli_entry_point(too_many_arguments)
