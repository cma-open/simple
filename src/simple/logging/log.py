"""Logger management for the package."""

# Some lines from
# https://stackoverflow.com/questions/11111064/how-to-set-different-levels-for-different-python-log-handlers
# https://stackoverflow.com/questions/10206178/how-can-i-log-the-package-name-in-python/72873684#72873684

import logging
import logging.config
from pathlib import Path

from simple.definitions import DEMO_TEMP_DIR

logging.config.dictConfig(
    {
        "version": 1,
        # Other configs ...
        "disable_existing_loggers": False,
    }
)

# Create log formatter
file_formatter = logging.Formatter(
    fmt="%(asctime)s :: %(name)s :: %(levelname)-8s "
    ":: %(message)s :: %(filename)s -> %(funcName)20s()",
    datefmt="%y-%m-%d %H:%M",
)

# Create console formatter
console_formatter = logging.Formatter(
    fmt="%(name)s :: %(levelname)-8s :: %(message)-35s",
)

# Reduced output for the simple config log
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


def add_system_log_file_handler(
    logger: logging.Logger, log_path: Path
) -> logging.Logger:
    """Add system log file handler to logger."""
    # Create main system log handler
    file_handler = logging.FileHandler(log_path, mode="w")
    # Set level for log file - debug and above
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


def add_config_log_file_handler(logger: logging.Logger, log_path: Path):
    """Add config log file handler to logger."""
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(config_file_formatter)
    # Add handler to the logger
    logger.addHandler(file_handler)
    return logger


def create_system_logger(log_path: Path):
    """Create the system logger."""
    # Get logger name
    logger = logging.getLogger("SystemLog")
    # Set initial level for the logger
    logger.setLevel(logging.DEBUG)
    # Add handlers to the logger
    add_system_console_handler(logger=logger)
    add_system_log_file_handler(logger=logger, log_path=log_path)
    return logger


def create_config_logger(log_path: Path):
    """Create the config logger."""
    # Get logger name
    logger = logging.getLogger("ConfigLog")
    add_config_log_file_handler(logger=logger, log_path=log_path)
    logger.setLevel(logging.DEBUG)
    return logger


# -------------------------------------------------------------------------------------

# TODO
# Add test tables


def demo_config_file_log(log_path):
    """Demo of log file write and content."""
    logger = create_config_logger(log_path=log_path)
    # Log message to write to the config log file
    logger.debug("Config demo_temp started")
    logger.info("Config demo_temp")
    logger.debug("Config demo_temp finished")


# TODO KISS - just chose debug levels and stick to them .....


def demo_system_console_log(log_path):
    """Demo of system console log write and content."""
    logger = create_system_logger(log_path=log_path)
    # All log messages go to log file
    # Info level and above go to console
    logger.debug("System demo_temp started")  # File only
    logger.info("System demo_temp")  # File and console
    logger.warning("System warning")  # File only
    logger.debug("System demo_temp finished")  # File only


if __name__ == "__main__":
    # Create DEMO_DIR if not yet existing
    DEMO_TEMP_DIR.mkdir(exist_ok=True)
    # Set within package location for demo_temp log file
    # Note - all log files are to be ignored via vcs
    demo_system_log = DEMO_TEMP_DIR / "demo_system.log"
    demo_system_console_log(log_path=demo_system_log)
    demo_config_log = DEMO_TEMP_DIR / "demo_config.log"
    demo_config_file_log(log_path=demo_config_log)
