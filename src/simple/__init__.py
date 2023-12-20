"""Simple python package.

Provide example code for training, testing, developing.

"""

import logging

# from simple.config.reader import return_datadir
from simple.logger.log import add_system_console_handler
from simple.setup.system_setup import system_setup

# Set logger name - at this level it is same as package name
logger_name = logging.getLogger(__name__)
# Set default logger level
logger_name.setLevel(logging.DEBUG)
# Set default console output logger
add_system_console_handler(logger=logger_name)

# TODO check potn for in memory log of post setup / pre app run


system_setup()
# setup_directories(datadir_root_path=return_datadir())
