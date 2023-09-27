"""Workflow for the simple analysis system."""

import logging

# from simple.common.common import clean_directory
from simple.config.reader import main
from simple.data.example.example import data_example

# Dev Notes

# KISS !

# note distinction python called vs command line at terminal
# system dependencies
# installed into appropriate location or environment

# step 0 (optional)
# -----------------

# user confirms or edits the system config
# this determines data and scratch (temp) directories
# log settings to file
# link to notes / discussion / issue
# if config setting should be committed as part of the repo?, separate repo?

# step 1
# ------

# create basic netcdf, CF compliant, with simple data content
# write to file (as specified by config)

# step 2
# ------

# view netcdf content
# describe content in high detailed, labeled, very descriptive


# step 3
# ------

# test netcdf compliance - both tools


# step x
# ------

# run cli tool X  to take user input and return analysis output to the terminal

# step y
# ------

# ? AMEND
# amend cli tool, or another to  take user input, conduct analysis and write to netcdf
# write netcdf to outputs dir
# log process, including record user inputs


# WORKFLOW  - EXAMPLE
# Initial example workflow to help build and testing
def worflow_main():
    """System workflow."""
    # Read config, create subdirectories, write config to log
    main()
    # Create new module level logger
    logger = logging.getLogger("SystemLog")
    # Start workflow
    logger.info("Worklow: started")
    # logging.info('logger Worklow: started')
    # Dummy data example function
    data_example()
    # Confirm and check datadir
    # Parse the user settings and determine current path
    # datadir_actual = return_datadir()

    # Clean up directories
    # clean_directory(dir_path=datadir_actual)

    # End of workflow
    logger.warning("Workflow: ended")
    # logging.warning("Check this !")


if __name__ == "__main__":
    worflow_main()
    # List all current logger for debugging dev
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    print(loggers)
