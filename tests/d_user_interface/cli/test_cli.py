"""Test the cli tool."""

# This module uses subprocess, which can raise security threats.
# The risk have been reviewed via Codacy, Bandit.
# The generic warning on import has been left active, in case of future edits here.
# Each specific use warning has been checked and then ignored, where safe to do so.
# bandit ignore command is # nosec, per line

import subprocess  # nosec  # bandit ignore
from pathlib import Path

from simple.definitions import PACKAGE, SRC_DIR

# Define cli filepath
CLI = Path(SRC_DIR, PACKAGE, "cli.py")
# No docstring for CLI, to avoid publishing system filepaths
MODULE = "simple.cli"
"""str: Module name."""
TOOL = "cli-simple"
"""str: Script command name."""

# Testing note
# cli tool is registered via entry points
# can't be called and run via filepath (as does not use main)
# can't be called and run via module name (as does not use main)
# See other d_user_interface tests for examples using these tests

# TODO - update the config file !!

# TODO - also test via calls to entrypoint function?


def test_cli_run_as_entrypoint():
    """Test the entrypoint script can be called.

    Allows verification that CLI tool is correctly installed (via setup.py)
    """
    # Note - the script tool name is set in the entry_points section of setup.py
    # TODO add a documentation cross ref here
    out = subprocess.run([TOOL, "--help"], check=True)  # nosec
    assert out.returncode == 0

    out = subprocess.run([TOOL, "--version"], check=True)  # nosec
    assert out.returncode == 0
