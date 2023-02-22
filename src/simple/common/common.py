"""Common system functions."""

from importlib.util import find_spec
from pathlib import Path

from simple.definitions import PACKAGE


def check_install_status(display=None):
    """Check if system is installed as user or editable develop install."""
    # Note - designed for src package structure
    spec = find_spec(PACKAGE)
    test_source = "src" in spec.origin
    test_site_packages = "site-packages" in spec.origin
    if test_source:
        if display:
            print(f"Editable install at: {spec.origin}")
        return "Editable"
    elif test_site_packages:
        if display:
            print(f"User install into site-packages at: {spec.origin}")
        return "User"
    else:
        return "Unknown path or not installed"


def clean_directory(dir_path, files):
    """Remove specified list of files from named directory."""
    for file in files:
        filepath = Path(dir_path) / file
        filepath.unlink(missing_ok=True)
