#!/bin/bash

#######################################################################################
# Script to uninstall the system
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
sleep 2

# Require the user to confirm
while true; do
    read -p "Do you want to uninstall the system?  " yn
    case $yn in
        [Yy]* )
          echo "---"
          echo "Uninstalling";
          cd ../..
          pwd
          pip uninstall ${PACKAGE}
          break;;
        [Nn]* )
          echo "---"
          echo "Exiting"
          exit;;
        * )
          echo "Please answer yes or no.";;
    esac
done
echo

#######################################################################################
# Code review and system context notes
# ====================================
#######################################################################################
