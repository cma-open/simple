#!/bin/bash

#######################################################################################
# Script to remove the conda environment
#######################################################################################

# Set code root directory as script constant (relative to this script)
CODE_DIR="$(dirname $(dirname "${PWD}"))"
echo
echo "Root: ${CODE_DIR}"

# ensure conda commands are accessible (required to run)
conda init bash > /dev/null 2>&1
eval "$(conda shell.bash hook)"

# Source variables from common
source "${CODE_DIR}/scripts/common/common.sh"
echo
echo "Removing conda environment with name: ${ENV_NAME}"
echo
echo "---------------------------------------"
echo "This may be a slow process > 5 mins "
echo "---------------------------------------"
echo
sleep 5
conda deactivate
conda env remove -n  "${ENV_NAME}"
echo " --------------------------------------------------"
