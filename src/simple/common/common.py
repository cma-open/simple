"""Common system functions."""

import importlib
from pathlib import Path


def check_install_status(display=None):
    """Check if system is installed as user or editable develop install."""
    spec = importlib.util.find_spec("simple")
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


def clean_directory(dir_path, files):
    """Remove specified list of files from named directory."""
    for file in files:
        filepath = Path(dir_path) / file
        filepath.unlink(missing_ok=True)
