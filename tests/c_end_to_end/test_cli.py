"""End to end tests for the cli tool."""

# End to end test notes
# Aim to test software from start to finish (as used by the user)
# If testing API, then make calls as clients would.

# This module uses subprocess, which can raise security threats.
# The risk have been reviewed via Codacy, Bandit.
# Each specific use warning has been checked and then ignored, where safe to do so.
# bandit ignore command is # nosec, per line

import subprocess  # nosec  # bandit ignore

from simple.config.reader import return_verbosity

TOOL = "cli-simple"
"""str: Script command name."""


def test_cli_run_as_user():
    """Test the CLI tool run end to end."""
    # Set user inputs
    uargs = "5", "5"
    # Use subprocess to run the tool with user inputs
    output = subprocess.run([TOOL, *uargs], capture_output=True, text=True)  # nosec
    # Print full output, for debug / example use if verbose editable install
    if return_verbosity():
        print("--")
        print(output)
        print("---")
    # Set expected calculation result, given supplied inputs
    expected = "['10.000005', '10.000005']"
    # Confirm CLI output is as expected
    assert output.stdout.strip() == expected  # strip newline from output
    # Confirm success returncode from CLI
    assert output.returncode == 0
