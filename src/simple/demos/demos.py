"""Code for all system demos.

Example:
-------
    demo_logs
    Two logs are created within a temp demo directory
    Allows easy viewing of log file format and content

    Called via command line as set in pyproject.toml

    $ demo-logs

"""
import logging
from pathlib import Path

from simple.common.common import debug_loggers
from simple.config.reader import return_datadir, return_verbosity
from simple.logger.log import (
    console_formatter,
    create_config_logger,
    create_system_logger,
)

system_logger = logging.getLogger(__name__)

# Set demo test constants
DEMO_TEMP_DIR = return_datadir() / "demo_temp"
# Set logger names
DEMO_CONFIG_LOGGER_NAME = "DemoConfigLog"
DEMO_SYSTEM_LOGGER_NAME = "DemoSystemLog"
# Set demo log filenames
DEMO_CONFIG_LOG_FILE = "demo_config.log"
DEMO_SYSTEM_LOG_FILE = "demo_system.log"


def demo_config_file_log(log_path):
    """Demo of log file write and content."""
    # No console handler so no terminal output
    logger = create_config_logger(
        log_path=log_path, logger_name=DEMO_CONFIG_LOGGER_NAME
    )
    # Log message to write to the config log file
    logger.debug("Config demo_temp started")
    logger.info("Config demo_temp")
    logger.debug("Config demo_temp finished")

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def demo_system_console_log(log_path: Path):
    """Demo of system console log write and content.

    Parameters
    ----------
    log_path : Path
       Full path to output log file

    Returns
    -------
    logger : logging.Logger
    """
    # Reminder - info level and above goes to console
    # debug level and above go to file
    # Reminder create_system_logger gets logger by name, but defaults to package logger
    # Then sets level and adds file handler only, it assumes that the console handler
    # exists already
    # Therefore for the DEMO - create a new logger instead of PACKAGE level logger
    # and add a system console handler
    # Set logger name - create new logger
    logger = logging.getLogger(DEMO_SYSTEM_LOGGER_NAME)
    # Set initial logging level (required)
    logger.setLevel(level=logging.DEBUG)
    # Add console handler
    # Set default handler name if no argument supplied
    handler_name = "DemoSystemConsoleHandler"
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
    file_handler_name = "DemoSystemFileHandler"
    # Update the demo logger with file logger
    create_system_logger(
        log_path=log_path,
        logger_name=DEMO_SYSTEM_LOGGER_NAME,
        file_handler_name=file_handler_name,
    )
    # All log messages go to log file
    # Additionally info level and above go to console
    logger.debug("System demo_temp started")  # File only
    logger.info("System demo_temp")  # File and console
    logger.debug("System demo_temp finished")  # File only
    return logger

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def demo_logs(demo_temp_dir=None):
    """Demo for log setup and creation."""
    # Dev Note - all log files should be ignored via vcs
    # Note - for dev install demo_temp will be within repo
    # Note - for a full install demo_temp will be within datadir root
    if demo_temp_dir is None:
        demo_temp_dir = DEMO_TEMP_DIR
    # Create DEMO_TEMP_DIR if not yet existing
    demo_temp_dir.mkdir(exist_ok=True)
    # Set full path location for demo_temp log files x2
    demo_system_log = demo_temp_dir / "demo_system.log"
    demo_config_log = demo_temp_dir / "demo_config.log"
    # Run the demo to create console logs - including demo log messages
    demo_system_console_log(log_path=demo_system_log)
    # Run the demo to create config file logs - including demo log messages
    demo_config_file_log(log_path=demo_config_log)
    # Add an extra log message at system level
    system_logger.info(f"Demo logs has run - see files in {demo_temp_dir}")
    # Optional show all current logger handlers as debugging or training example
    if return_verbosity():
        debug_loggers()
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit
    # b_integration
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================
