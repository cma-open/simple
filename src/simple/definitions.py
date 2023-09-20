"""Common code constants.

.. module: definitions
Generates main package name and directory for use by other modules.

"""

from importlib.resources import files
from pathlib import Path

# Set the package name
# TODO check r.e. take name from setup.py to minimise duplication - check after toml
# TODO take name from package
PACKAGE = "simple"
# TODO refactor to give full path or as new RESORCES_DIR
# Set namespace subpackage holding resource files
RESOURCES = f"{PACKAGE}.resources"

# Set the directory paths relative to this file
# Note - only parent package dir is reliable for use in both user and dev installs
# repo/src/package (dev, editable) and site-packages/package (full install)
PACKAGE_DIR = files(PACKAGE)
# Root dir gives src (dev, editable) and site-packages (full install)
ROOT_DIR = Path(files(PACKAGE)).parent

RESOURCES_DIR = ROOT_DIR / PACKAGE / "resources"
DEMO_DIR = ROOT_DIR / PACKAGE / "demo"

# ===================================================================
# Test type and location (training use)
# ===================================================================
# a_unit            test_definitions.py
# b_integration     n/a
# c_end_to_end      n/a
# d_user_interface  n/a
# ===================================================================


#####################################################################
# Architecture / design / code review notes (training use)
# -------------------------------------------------------------------
# Code is designed as modular to allow adaptation and reuse
# e.g. PACKAGE variable use
#####################################################################
