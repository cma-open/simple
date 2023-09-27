#!/bin/bash

#######################################################################################
# Script to run system tests - report coverage to terminal
#######################################################################################

# Source code, variables from tests/common.sh
# Makes CODE_DIR etc available. Also sources common/common.sh
source common.sh
echo "Current working directory: ${PWD}"
echo "Move to test dir and run pytest with coverage: ${TESTS_DIR}"
echo "Run coverage against package name: ${PACKAGE}"

cd "${TESTS_DIR}"

# TODO check install vs dev test coverage reports
# run tests with coverage output
pytest --cov-config="${CODE_DIR}/.coveragerc"  \
       --cov-report term \
       --cov="${PACKAGE}"
       # note uses PACKAGE to cover both install types

#######################################################################################
# Code review and system context notes
# ====================================
# This script is used during manual testing
# Not called by any other scripts,
# not used as part of the GitHub actions automated tests
#######################################################################################
