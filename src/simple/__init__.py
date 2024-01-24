"""Simple python package.

Provide example code for training, testing, developing.

"""

import logging

from simple.logger.log import add_system_console_handler
from simple.setup.system_setup import system_setup

# Set logger name - at this level it is same as package name
logger_name = logging.getLogger(__name__)
# Set initial logging level (required)
logger_name.setLevel(level=logging.DEBUG)
# Set default console output logger (allows initial general logging to terminal)
add_system_console_handler(logger=logger_name)

# TODO check potn for in memory log of post setup / pre app run
# Run system setup to create required directories and log files
system_setup()
