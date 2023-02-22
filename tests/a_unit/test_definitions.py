"""Tests for the definitions module."""

from simple.definitions import PACKAGE, PACKAGE_DIR, RESOURCES

DEBUG = False


def test_definitions():
    """Test for definitions module."""
    assert PACKAGE == "simple"
    assert RESOURCES == "simple.resources"
    dev_path = "simple/simple/src/simple"
    user_path = "site-packages/simple"
    assert (dev_path in PACKAGE_DIR) or (user_path in PACKAGE_DIR)
    # optional print out info to test report
    # TODO consider aut enable all debug for editable not user installs?
    if DEBUG:
        print(f"Package dir: {PACKAGE_DIR}")
        print(f"Package name: {PACKAGE}")
        print(f"Package resources: {RESOURCES}")
