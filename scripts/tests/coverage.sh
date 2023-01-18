#!/bin/bash

#######################################################################################
# Script to run system tests - report coverage to terminal
#######################################################################################

# Source code, variables from common.sh
source common.sh

echo "Current working directory: ${PWD}"

# ensure conda commands are accessible
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

# activate conda env
conda activate "simple-env"

# run tests with coverage output
pytest --cov-config="${CODE_DIR}/.coveragerc"  \
       --cov-report term \
       --cov="${CODE_DIR}" "${TESTS_DIR}"

#######################################################################################
# Code review and system context notes
# ====================================
# This script is used during manual testing
# Not called by any other scripts,
# not used as part of the GitHub actions automated tests
#######################################################################################
