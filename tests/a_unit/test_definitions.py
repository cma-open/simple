"""Tests for the definitions module."""

from simple.config.reader import return_verbosity
from simple.definitions import PACKAGE, PACKAGE_DIR, RESOURCES, ROOT_DIR


def test_definitions_constants():
    """Test for definitions module."""
    assert PACKAGE == "simple"
    assert RESOURCES == "simple.resources"


def test_definitions_directories():
    """Test for definitions module."""
    # Optional, print further info to tests if verbose set on editable installs
    if return_verbosity():
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
