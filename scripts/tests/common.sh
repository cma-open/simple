#!/bin/bash

#######################################################################################
# Script to hold common code used by the test scripts
#######################################################################################

# ensure conda commands are accessible
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

# Set python package root dir as script constant
# Used by the other test scripts
readonly CODE_DIR="$(dirname "$(dirname "${PWD}")")"

# Source variables from common
source "${CODE_DIR}/scripts/common/common.sh"

# activate conda env
conda activate ${ENV_NAME}

# Set coverage config file as script constant
# Set here, rather than common/common, as relative to CODE_DIR
readonly COV_CONFIG="${CODE_DIR}"/.coveragerc

# Get location of the installed package
# (local if editable install, site-packages if full install)
# reminder - double quotes, to allow interpolation
COMMAND=("import inspect; import pathlib; import ${PACKAGE}; \
package = pathlib.Path(inspect.getfile(${PACKAGE})); \
print(str(package.parent)) ")

# Set package dir name
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
