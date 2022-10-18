#!/bin/bash

#######################################################################################
# Script to hold common code used by the test scripts
#######################################################################################

# ensure conda commands are accessible
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

# activate conda env
conda activate "simple-env"

# Set python package root dir as script constant
readonly CODE_DIR="$(dirname "$(dirname "${PWD}")")"
readonly PACKAGE="simple"
# Set coverage config file as script constant
readonly COV_CONFIG="${CODE_DIR}"/.coveragerc

# Get location of the installed package
# (local if editable install, site-packages if full install)
# reminder - double quotes, to allow interpolation
COMMAND=("import inspect; import pathlib; import ${PACKAGE}; \
package = pathlib.Path(inspect.getfile(${PACKAGE})); \
print(str(package.parent)) ")

PACKAGE_DIR=$(python -c "${COMMAND}")


# Set tests directory
readonly TESTS_DIR="${CODE_DIR}"/tests

echo " ---- * ----"
echo "Running system tests with pytest"
echo "Package: ${PACKAGE}"
echo "Script source package root directory: ${CODE_DIR}"
echo "Installed package root directory: ${PACKAGE_DIR}"
echo "Script tests directory: ${TESTS_DIR}"
echo "Coverage config file: ${COV_CONFIG}"
echo " ---- * ----"

#######################################################################################
# Code review and system context notes
# ====================================
# Further refactor could extract code into functions
#######################################################################################
