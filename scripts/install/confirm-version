#!/bin/bash

#######################################################################################
# Script to confirm current package version  - for dev / debug use
#######################################################################################

# Set python package code dir as script constant (relative to this script)
readonly CODE_DIR="$(dirname "$(dirname "${PWD}")")"
# Source variables from common
source "${CODE_DIR}/scripts/common/common.sh"

echo "Activating the conda environment: ${ENV_NAME}"
echo
# ensure conda commands are accessible (required to run)
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"
conda activate  "${ENV_NAME}"

# Show current version
pip show "simple" | grep Version
