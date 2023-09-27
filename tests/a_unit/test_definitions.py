"""Tests for the definitions module."""

from simple.definitions import PACKAGE, PACKAGE_DIR, RESOURCES, ROOT_DIR

DEBUG = True


def test_definitions_constants():
    """Test for definitions module."""
    assert PACKAGE == "simple"
    assert RESOURCES == "simple.resources"


def test_definitions_directories():
    """Test for definitions module."""
    # Optional, print info to tests
    # TODO consider auto enable all debug for editable not user installs?
    # See #36
    if DEBUG:
        print(f"Package name: {PACKAGE}")
        print(f"Package resources: {RESOURCES}")
        print(f"Package dir: {PACKAGE_DIR}")
        print(f"Root dir: {ROOT_DIR}")

    dev_path = "simple/simple/src/simple"
    user_path = "site-packages/simple"
    assert (dev_path in str(PACKAGE_DIR)) or (user_path in str(PACKAGE_DIR))

    dev_root = "simple/simple/src"
    user_root = "site-packages"
    assert (dev_root in str(ROOT_DIR)) or (user_root in str(ROOT_DIR))
