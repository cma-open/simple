"""End to end tests for the system demos."""

# End to end test notes
# Aim to test software from start to finish (as used by the user)
# If testing API, then make calls as clients would.

# This module uses subprocess, which can raise security threats.
# The risk have been reviewed via Codacy, Bandit.
# Each specific use warning has been checked and then ignored, where safe to do so.
# bandit ignore command is # nosec, per line

import subprocess  # nosec  # bandit ignore

from simple.definitions import DEMO_TEMP_DIR, PACKAGE_DIR


def test_demo_system_log():
    """Test the demo_temp for the system log."""
    # Remove any existing demo_temp log files
    demo_files = list(DEMO_TEMP_DIR.iterdir())
    for demo_file in demo_files:
        demo_file.unlink(missing_ok=True)
    # Confirm the directory was emptied
    assert any(DEMO_TEMP_DIR.iterdir()) is False
    log_main = str(PACKAGE_DIR / "logging" / "log.py")
    output = subprocess.run(
        ["python", log_main], capture_output=True, text=True
    )  # nosec
    test_config_log_file = DEMO_TEMP_DIR / "demo_config.log"
    test_system_log_file = DEMO_TEMP_DIR / "demo_system.log"
    # Test file was created
    assert test_config_log_file.is_file()
    assert test_system_log_file.is_file()
    # Check console log output is as expected
    expected = (
        "SystemLog :: INFO     :: System demo_temp                   \n"
        "SystemLog :: WARNING  :: System warning                     \n"
    )
    assert output.stderr == expected

    # TODO expand tests to also read log file content on disk
    # TODO double check any option to mock out demo_temp dir
    #  e.g. via subprocess, not possible?
