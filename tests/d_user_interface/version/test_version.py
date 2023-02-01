"""Tests for package version."""

from importlib.metadata import PackageNotFoundError, version

from simple.definitions import PACKAGE

try:
    __version__ = version(PACKAGE)
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"


def test_installed_version():
    """Test package version is named."""
    assert __version__ != "unknown"
    print(__version__)
