"""Common code constants.

.. module: definitions
Currently used to generate main package name and directory
for use by other modules.

"""

import os

# Set the directory paths relative to this file
# Note - only parent dir is reliable for use in user vs dev installs
# repo/src/package (dev, editable) or site-packages/package (user)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# Do not use refs to SRC_DIR or REPO_DIR (historical context note)
# Set the package name
# TODO check r.e. take name from setup.py to minimise duplication
PACKAGE = "simple"
# Set namespace subpackage holding resource files
RESOURCES = f"{PACKAGE}.resources"
