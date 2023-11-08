#!/bin/bash

#######################################################################################
# Script to hold common code used by scripts
# Library script, not executable
#######################################################################################

# Assume CODE_DIR is always set by the calling script

# Set script constants
readonly SRC_DIR="${CODE_DIR}/src"
readonly SCRIPTS_DIR="${CODE_DIR}/scripts"
readonly PACKAGE="simple"  # note package name here !
readonly ENV_NAME="simple-env"
# Set name of environment file holding dependencies list
readonly CONDA_ENV_FILE='environment.yml'

echo " ---- * ----"
echo "Package name: ${PACKAGE}"
echo "Package root directory: ${CODE_DIR}"
echo "Source (src) directory: ${SRC_DIR}"
echo "Scripts directory: ${SCRIPTS_DIR}"
echo "Conda env file: ${CONDA_ENV_FILE}"
echo "Conda env name: ${ENV_NAME}"
echo " ---- * ----"

#######################################################################################
# Code review and system context notes
# ====================================
#######################################################################################
