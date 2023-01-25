#!/bin/bash

#######################################################################################
# Script to hold common code used by scripts
#######################################################################################

# Assume CODE_DIR is always set by the calling script

# Set script constants
readonly SRC_DIR="${CODE_DIR}/src"
readonly SCRIPTS_DIR="${CODE_DIR}/scripts"
readonly PACKAGE="simple"  # note package name here !
readonly ENV_NAME="simple-env"

echo " ---- * ----"
echo "Package name: ${PACKAGE}"
echo "Package root directory: ${CODE_DIR}"
echo "Source (src) directory: ${SRC_DIR}"
echo "Scripts directory: ${SCRIPTS_DIR}"
echo " ---- * ----"

#######################################################################################
# Code review and system context notes
# ====================================
#######################################################################################
