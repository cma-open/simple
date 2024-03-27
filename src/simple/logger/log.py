"""Logger management for the package."""

# Note - only the config logger uses a set specified name
# All other loggers, e.g. system logger use package or module names
# Some lines from
# https://stackoverflow.com/questions/11111064/how-to-set-different-levels-for-different-python-log-handlers
# https://stackoverflow.com/questions/10206178/how-can-i-log-the-package-name-in-python/72873684#72873684

import logging
import logging.config
from pathlib import Path

from simple.definitions import PACKAGE

# Set logger names
CONFIG_LOGGER_NAME = "ConfigLog"
# Reminder - system logger uses package or module name, not set directly

# Set main log filenames as module constants
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
# System console logs don't include timestamps
console_formatter = logging.Formatter(
    fmt="%(name)-28s: %(levelname)-8s: %(message)s",
)

# Reduced output for the simple config log file
# Gives timestamp and message (no module name)
config_file_formatter = logging.Formatter(
    fmt="%(asctime)s %(message)s",
    datefmt="%y-%m-%d %H:%M",
)


def add_system_console_handler(
    logger: logging.Logger, handler_name: str = None
) -> logging.Logger:
    """Add system console handler to logger.

    Parameters
    ----------
    logger : logging.Logger
        Logger object to which system console handler will be added
    handler_name : str (optional)
        Name of the stream handler, defaults to None


    Returns
    -------
    logging.Logger
        Updated logger with formatted stream handler added

    """
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "SystemConsoleHandler"
    # Create console log stream handler
    console_handler = logging.StreamHandler()
    # Name the console handler via argument or default
    console_handler.name = handler_name
    # Set level for console outputs - only info level and above
    console_handler.setLevel(logging.INFO)
    # Set the output format for the logger content
    console_handler.setFormatter(console_formatter)
    # Add handler to the logger
    logger.addHandler(console_handler)
    return logger
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            logger/test_system_log.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def add_system_log_file_handler(
    logger: logging.Logger, log_path: Path, handler_name: str = None
) -> logging.Logger:
    """Add system log file handler to logger.

    Parameters
    ----------
    logger : logging.Logger
        Logger object to which file handler will be added
    log_path : Path
        Full path to log filename
    handler_name : str (optional)
        Name of the file handler, defaults to None

    Returns
    -------
    logging.Logger
        Updated logger with formatted log file handler added
    """
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "SystemFileHandler"
    # Create main system log handler
    file_handler = logging.FileHandler(log_path, mode="a")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set level for log file - debug and above
    file_handler.setLevel(logging.DEBUG)
    # Add content formatter to the logger
    file_handler.setFormatter(file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            logger/test_system_log.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def create_system_logger(
    log_path: Path, logger_name: str = None, file_handler_name: str = None
) -> logging.Logger:
    """Create the system logger.

    Parameters
    ----------
    log_path : Path
        Full path to log filename
    logger_name : str
        Name of the created logger
    file_handler_name : str (optional)
        Name of the file handler, defaults to None
    Returns
    -------
    logging.Logger
        Created system logger
    """
    # Set default logger name if no argument supplied
    if logger_name is None:
        logger_name = PACKAGE
    # Get logger name from argument or default
    logger = logging.getLogger(logger_name)
    # Set initial level for the logger
    logger.setLevel(logging.DEBUG)
    # Add handlers to the logger
    # info level and above goes to console (already set by init)
    # debug level and above go to file
    add_system_log_file_handler(
        logger=logger, log_path=log_path, handler_name=file_handler_name
    )
    return logger
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            logger/test_system_log.py
    # b_integration     test_system_log.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


# ---
# config logger
# ---


def add_config_log_file_handler(
    logger: logging.Logger, log_path: Path, handler_name: str = None
) -> logging.Logger:
    """Add config log file handler to logger.

    Parameters
    ----------
    logger  : loggig.Loggger
        Logger to which handler will be added
    log_path : Path
        Full path to log filename
    handler_name : str (optional)
        Name of the file handler, defaults to None

    Returns
    -------
    logging.Logger
        Created system logger
    """
    # Set default handler name if no argument supplied
    if handler_name is None:
        handler_name = "ConfigFileHandler"
    file_handler = logging.FileHandler(log_path, mode="w")
    # Name the console handler via argument or default
    file_handler.name = handler_name
    # Set logging level
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(config_file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            logger/test_config_log.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def create_config_logger(log_path: Path, logger_name: str = None):
    """Create the config logger.

    Parameters
    ----------
    log_path : Path
        Full path to log filename
    logger_name : str
        Name of the created logger

    Returns
    -------
    logging.Logger
        Created system logger
    """
    if logger_name is None:
        logger_name = CONFIG_LOGGER_NAME
    # Get logger by name
    logger = logging.getLogger(logger_name)
    add_config_log_file_handler(logger=logger, log_path=log_path)
    logger.setLevel(logging.DEBUG)
    return logger
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            logger/test_config_log.py
    # b_integration     test_config_log.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================
