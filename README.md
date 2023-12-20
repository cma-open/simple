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
        - Code standards and style
            - black
            - PEP8
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
        - cd scripts/conda
        - ./create-env
        - cd scripts/install
        - ./install

    - Usage
        - make sure the environment has been activated
            - conda activate simple-env
        - system workflow: run these from the command line
            - cli-simple
                - Custom analysis calculation on two supplied integers
                - A simple example of an argparse command line tool
            - confirm-config
                - prints the chosen config  to terminal
                - this command does not use the log files
            - system-setup
                - Sets up the system ready for use
                - Logs the config to file, begins detailed system use logging
                - Creates the required system directories (as set in the config)
            - create-data
                - creates a test.nc netcdf file in outputs dir
            - create-data-options
                - creates a test.nc netcdf file in ouputs dir
                - has user options e.g. --verbose
            - clean
                - removes the set of data files that were created within outputs
            - demo_logs
                - Creates both config and system demo logs in a temp directory


Development and testing

    - Install via the script and follow the prompts
        - cd scripts/install
        - ./install
    - Tests run via
        - cd scripts/tests
        - ./test
        - ./dev-test (runs tests with report of currently failing tests)
    - Test coverage checked via
        - cd scripts/tests
        - ./coverage

System design, content, and architecture

    - docstrings are added to tests, against convention, to aid display via sphinx
    - tests are not always realistic, the system is over-tested as a training example
    - system features are chosne to illustrate training examples, so not always realistic
    - features may be duplicated to allow different solutions to be compared

Codestyle code quality and code review

    - PEP8, black
    - Google shell script standard
        - (lib vs executable)
    - automated tests run via GitHub actions
    - branch based development with code review per pull request

Branches and releases

    - Manual releases via the CalVer system
    - Dev branches named by feature number
    - Dev system version will be named automatically via setuptools scm

Logging strategy

    - System contains a logger subpackage and a log module
    - Two log files are created
      - config.log
      - system.log

    - The Config log is specialised and has limited use.
    - This log is referenced directly by name: ConfigLog
    - ConfigLog (config.log) holds a record of current system configuration
       and installation settings. This logger only holds a file handler
      therefore all calls are output to file not to the terminal.
      The file is set to overwrite each time it is run.

    - The main system Log (system.log) uses both a console logger and file handler.
      Information is output to both terminal console and to file.
      INFO level and above go to the console.
      DEBUG and above go to file.
      Therefore more detailed logging is available by checking the system.log file.

      A verbose setting is used to deselect some log output if set to False. This can
      make logs smaller and easier to read. If needed for additional debugging this can
      be set to True and will cause further debug messages to be logged.
      The verbose settign only applies to developer editable installs not full user use.
      (Reminder DEBUG>INFO>WARNING>ERROR>CRITICAL)

Wiki

    - Not used in this repo
