"""Common code constants.

.. module: definitions
Currently used to generate main code source root path and package name
for use by other modules.

"""

import os

# Set the directory paths relative to this file
# Note - only parent dir is reliable for use in user vs dev installs
# repo/src/package (dev) or site-packages/package (user)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
# Do not use refs to SRC_DIR or REPO_DIR

# Set the package name
# TODO check r.e. take name from setup.py to minimise duplication
PACKAGE = "simple"

if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement.
    print(f"definitions file: {os.path.abspath(__file__)}")
    print(f"package dir: {PACKAGE_DIR}")
