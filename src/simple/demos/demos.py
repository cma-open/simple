"""Code for all system demos."""
import logging

from simple.common.common import debug_loggers
from simple.config.reader import return_verbosity
from simple.definitions import DEMO_TEMP_DIR
from simple.logger.log import (
    add_system_console_handler,
    create_config_logger,
    create_system_logger,
)

system_logger = logging.getLogger(__name__)

# TODO KISS - just chose debug levels and stick to them .....


def demo_config_file_log(log_path):
    """Demo of log file write and content."""
    logger = create_config_logger(log_path=log_path)
    # Log message to write to the config log file
    logger.debug("Config demo_temp started")
    logger.info("Config demo_temp")
    logger.debug("Config demo_temp finished")


def demo_system_console_log(log_path):
    """Demo of system console log write and content."""
    # Note demo system logs are named as DEMOLog
    logger = create_system_logger(log_path=log_path, logger_name="DEMOLog")
    # Add a console handler - this mimics the one created for the system in
    add_system_console_handler(logger=logger)
    # All log messages go to log file
    # Additionally info level and above go to console
    logger.debug("System demo_temp started")  # File only
    logger.info("System demo_temp")  # File and console
    logger.debug("System demo_temp finished")  # File only


def demo_logs():
    """Demo for log setup and creation."""
    # Dev Note - all log files should be ignored via vcs
    # Create DEMO_DIR if not yet existing
    DEMO_TEMP_DIR.mkdir(exist_ok=True)
    # Set within package location for demo_temp log files x2
    demo_system_log = DEMO_TEMP_DIR / "demo_system.log"
    demo_config_log = DEMO_TEMP_DIR / "demo_config.log"
    # Run the demo to create console logs
    demo_system_console_log(log_path=demo_system_log)
    # Run the demo to create config file logs
    demo_config_file_log(log_path=demo_config_log)
    system_logger.info(f"Demo logs has run - see files in {DEMO_TEMP_DIR}")
    # Optional show all current logger handlers as debugging or training example
    if return_verbosity():
        debug_loggers()

    # TODO
    # amend to prevent the calls from these demo logs going over to the main system log
    # START
