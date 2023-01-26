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
        - Simple config file use
        - Basic log files

User instructions

  - Checkout
    - Checkout the code locally from the GitHub repo

  - Config
    - Open src/simple/config.ini and set datadir and scratchdir or retain defaults
    - If any config is changed later, then re-install and run through the workflow again

  - Installation
    - scripts/conda/create-env.sh
    - scripts/install/install.sh

  - Usage
    - workflow
      - confirm_config: print and log config settings
      - create-data:
      - create-data-options:
      - clean: remove data files

Todo
  - check google shell script standard - lib vs executable


Fixes - next steps
  - note about pip show nd pip uninstal errors
