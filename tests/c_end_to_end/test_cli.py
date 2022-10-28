"""End to end test for the cli tool."""

# End to end test notes
# Aim to test software from start to finish (as used by the user)
# If testing API, then make calls as clients would.

import subprocess

DEBUG = False

TOOL = "cli-simple"
"""str: Script command name."""


def test_cli_run_as_user():
    """Test the CLI tool run end to end."""
    # example user input args
    uargs = "5", "5"
    out = subprocess.run([TOOL, *uargs], capture_output=True, text=True)  # nosec
    if DEBUG:
        print("--")
        print(out)
        print("---")
    expected = "['10.000005', '10.000005']"
    assert out.stdout.strip() == expected  # strip newline from output
    assert out.returncode == 0
