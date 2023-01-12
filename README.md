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
    - Good code quality
    - Automated testing (GitHub workflow actions)
    - Use of conda environment
    - Simple config file use

Checkout
- Checkout the code locally from the GitHub repo

Config
- Open src/simple/config.ini and set datadir and scratchdir or retain defaults
- If any config is changed later, then re-install and run through the workflow again

Installation
- scripts/conda/create-env.sh
- scripts/install/install.sh

Use
- workflow
    - confirm_config: print and log config settings
    -
- commands = ....


Today
- system installs and works - remove hotfixes (CA)
- check google shell script standard - lib vs executable


Fixes - next steps
- restart / reset/ closed pycharm etc
- work out why install and uninstall not working
- add new uninstall script
- log and print all swetup details


- editable locla install = uses within repo dirs automatically
- user install requires a dir to be set in config, but will default to tilde
-
