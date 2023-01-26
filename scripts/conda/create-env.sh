#!/bin/bash

#######################################################################################
# Script to create named conda environment
# Uses environment.yml file
#######################################################################################

# Set code root directory as script constant
CODE_DIR="$(dirname $(dirname "${PWD}"))"

# Source variables from common
source "${CODE_DIR}/scripts/common/common.sh"

# ensure conda commands are accessible (required to run)
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

echo "Creating conda environment from: ${CONDA_ENV_FILE}"
conda env create -f "${CODE_DIR}/${CONDA_ENV_FILE}"

echo " --------------------------------------------------"
