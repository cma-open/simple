"""Common code constants.

.. module: definitions
Currently used to generate main package name and directory
for use by other modules.

"""

import os

# Set the directory paths relative to this file
# Note - only parent dir is reliable for use in both user and dev installs
# repo/src/package (dev, editable) or site-packages/package (user)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the package name
# TODO check r.e. take name from setup.py to minimise duplication
PACKAGE = "simple"
# Set namespace subpackage holding resource files
RESOURCES = f"{PACKAGE}.resources"

# ==================================================================================
# Test type and location (training use)
# ----------------------------------------------------------------------------------
# a_unit  test_definitions.py
# b_integration  n/a
# c_end_to_end  n/a
# d_user_interface  n/a
# ==================================================================================

# ==================================================================================
# Architecture / design / code review notes
# ----------------------------------------------------------------------------------
# Code is designed as overly modular to allow potential adaptation and reuse
# e.g. PACKAGE variable use
# ==================================================================================
