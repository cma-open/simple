# simple
A very simple python package with a command line tool

[![](https://github.com/cma-open/simple/workflows/tests/badge.svg)](https://github.com/cma-open/simple/actions)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/807d755085924a0d8b788c7578eccd92)](https://www.codacy.com/gh/cma-open/simple/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cma-open/simple&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/807d755085924a0d8b788c7578eccd92)](https://www.codacy.com/gh/cma-open/simple/dashboard?utm_source=github.com&utm_medium=referral&utm_content=cma-open/simple&utm_campaign=Badge_Coverage)

Repo content

    - A working, installable python package
    - Contains command line tools
    - Contains a main system processing workflow
    - Illustrates
        - Good test coverage (pytest)
        - Good code quality (Codacy)
        - Automated testing (GitHub workflow actions)
        - Use of conda environment
        - Simple config file use (WIP)
        - Basic log files (WIP)

User instructions

    - Prerequisites
        - conda must be installed and available to the system

    - Checkout
        - Checkout the code locally from the GitHub repo

    - Config
        - Open src/simple/config.ini and set datadir (or retain defaults)
        - Note if default config is used then data will write to home (~)
        - Note if an editable install is selected (see installation)
             - config setting are ignored
             - data is written within the repo directory structure
        - If any config is changed later, then re-install and run through the workflow again

    - Installation
        - scripts/conda/create-env.sh
        - scripts/install/install.sh

    - Usage
        - workflow: run these from the command line, within the activated conda environment
            - confirm-config
                - prints and logs the chosen config settings
            - create-data
                - creates a test.nc netcdf file in outputs dir
            - create-data-options
                - creates a test.nc netcdf file in ouputs dir
                - has user options e.g. --verbose
            - clean
                - removes the set of data files that were created within outputs

Todo

    - check google shell script standard - lib vs executable

Fix next steps

    - note about pip show nd pip uninstall errors

Code review and system architecture

    - docstrings are added to tests, against convention, to aid display via sphinx
    - tests are not always realistic, the system is over-tested as a training example
