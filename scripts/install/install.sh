#!/bin/bash

#######################################################################################
# Script to install the system
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
echo

echo "Install the system: via developer or user option"
echo "Select Y only for one of the two following options"
echo
echo "Consider: are you developing the system, or are you an end user?"
echo
sleep 2

# Require the user to confirm
while true; do
    read -p "Do you want to install the system as a developer for further development?  " yn
    case $yn in
        [Yy]* )
          echo "---"
          echo "Installing - development mode";
          cd ../..
          pwd
          pip install -e . -v
          break;;
        [Nn]* )
          echo "---"
          # Require the user to confirm
          while true; do
              read -p "Do you want to install the system as an end user?  " yn
              case $yn in
                  [Yy]* )
                    echo "---"
                    echo "Installing system for end use";
                    cd ../..
                    pwd
                    pip install . -v
                    break 2;;
                    # break from both nested loops
                  [Nn]* )
                    echo "---"
                    echo "Exiting"
                    exit;;
                  * )
                    echo "Please answer yes or no.";;
              esac
          done;;
        * )
          echo "Please answer yes or no.";;
    esac
done
echo

#######################################################################################
# Code review and system context notes
# ====================================
# various install options
# python3 -m pip install -e git+https://git.repo/some_pkg.git#egg=SomeProject
# Installing from local src in Development Mode, i.e. in such a way that the project
# appears to be installed, but yet is still editable from the src tree.
# python3 -m pip install -e <path>
# normal install from within a src
# python3 -m install <path>
#######################################################################################
