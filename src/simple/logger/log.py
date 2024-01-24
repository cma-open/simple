"""Logger management for the package."""

# Some lines from
# https://stackoverflow.com/questions/11111064/how-to-set-different-levels-for-different-python-log-handlers
# https://stackoverflow.com/questions/10206178/how-can-i-log-the-package-name-in-python/72873684#72873684

import logging
import logging.config
from pathlib import Path

from simple.definitions import PACKAGE

# Set main config filename
CONFIG_LOG_FILE = "config.log"
SYSTEM_LOG_FILE = "system.log"

# Reminder -
# Set format for log message construction
# asctime (display the date and time of an event)
# levelname (severity), message (event description, including variable data)
# funcName (Name of function containing the logging call)
# module (Module (name portion of filename)
# Reminder-order DEBUG>INFO>WARNING>ERROR>CRITICAL
# TODO - take from config file
# see https://docs.python.org/3/howto/logging.html#logging-to-a-file


# Create log formatter
file_formatter = logging.Formatter(
    fmt="%(asctime)s : %(name)s : %(levelname)s "
    ": %(message)s : %(filename)s -> %(funcName)s()",
    datefmt="%y-%m-%d %H:%M",
)

# Create console formatter (main package system log)
# console logs don't include timestamps
console_formatter = logging.Formatter(
    fmt="%(name)-28s: %(levelname)-8s: %(message)s",
    # fmt="%(name)-21s :: %(levelname)-8s :: %(message)-35s",
)

# Reduced output for the simple config log
# Gives timestamp and message (no module name)
config_file_formatter = logging.Formatter(
    fmt="%(asctime)s %(message)s",
    datefmt="%y-%m-%d %H:%M",
)


def add_system_console_handler(logger: logging.Logger) -> logging.Logger:
    """Add system console handler to logger."""
    # Create console log handler
    console_handler = logging.StreamHandler()
    # Set level for console outputs - only info level and above
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    # Add handler to the logger
    logger.addHandler(console_handler)
    return logger

    # note tests
    # location
    # No longer used ?
    # TODO- Y still used by init


def add_system_log_file_handler(
    logger: logging.Logger, log_path: Path
) -> logging.Logger:
    """Add system log file handler to logger."""
    # Create main system log handler
    file_handler = logging.FileHandler(log_path, mode="a")
    # Set level for log file - debug and above
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


def create_system_logger(log_path: Path, logger_name: str = None):
    """Create the system logger."""
    # TODO docstring

    # Get logger
    if logger_name is None:
        logger_name = PACKAGE
    logger = logging.getLogger(logger_name)
    # Set initial level for the logger
    logger.setLevel(logging.DEBUG)
    # Add handlers to the logger
    # info level and above goes to console
    # debug level and above go to file
    add_system_log_file_handler(logger=logger, log_path=log_path)
    return logger


# ---
# config logger
#
def add_config_log_file_handler(logger: logging.Logger, log_path: Path):
    """Add config log file handler to logger."""
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(config_file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


def create_config_logger(log_path: Path):
    """Create the config logger."""
    # Get logger name
    logger = logging.getLogger("ConfigLog")
    add_config_log_file_handler(logger=logger, log_path=log_path)
    logger.setLevel(logging.DEBUG)
    return logger
