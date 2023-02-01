#!/bin/bash

#######################################################################################
# Script to run all system tests
# Invoking tests via pytest
# Called imported code will differ if local editable vs user install
#######################################################################################

# Source code, variables from common.sh
# Makes CODE_DIR etc available. Also sources common/common.sh
source common.sh

echo "Current working directory: ${PWD}"

# ensure conda commands are accessible
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

# activate conda env
conda activate "${ENV_NAME}"

# Discover and run tests on code path. Options include:
# -v verbose flag, -r displays “short test summary info” at end of session,
# -A lists all info
# --tb traceback print mode (auto/long/short/line/native/no)., e.g. --tb=long
pytest --tb=long -vrA  "${TESTS_DIR}"

#######################################################################################
# Code review and system context notes
# ====================================
# This script is used during manual testing
# Not called by any other scripts,
# not used as part of the GitHub actions automated tests
# Config options
#   - currently the pyproject.toml options take precedence over these script options
#   - retained here so later the config in pyproject.toml can be relaxed or removed
#######################################################################################
