"""Common code constants.

.. module: definitions
Currently used to generate main code source root path and package name
for use by other modules.

"""

import os

# Set the directory paths relative to this file
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the package name
# TODO check r.e. take name from setup.py to minimise duplication
PACKAGE = "simple"

if __name__ == "__main__":
    print(ROOT_DIR)
    print(PACKAGE_DIR)
    print(REPO_DIR)
