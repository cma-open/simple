"""Reader module for system config ini file."""

import configparser
import logging
from pathlib import Path

from simple.common.common import check_install_status
from simple.definitions import PACKAGE_DIR, ROOT_DIR
from simple.logging.log import create_config_logger, create_system_logger

# Set main config filename
CONFIG_LOG_FILE = "config.log"
SYSTEM_LOG_FILE = "system.log"
# Set logging config (TODO move)

# Set format for log message construction
# asctime (display the date and time of an event)
# levelname (severity), message (event description, including variable data)
# funcName (Name of function containing the logging call)
# module (Module (name portion of filename)


# Reminder-order DEBUG>INFO>WARNING>ERROR>CRITICAL
# TODO - take from config file
# see https://docs.python.org/3/howto/logging.html#logging-to-a-file


# Set module level logger
logger = logging.getLogger(__name__)

# Create configparser object
config = configparser.ConfigParser()
# Set path to user edited config file
configfile = f"{PACKAGE_DIR}/config.ini"
# Not supplied with docstring so filepath is not visible in sphinx docs

# Add note here and link to the package system strategy for logging
# e.g. log output, file vs. terminal, module level etc.


DEBUG = True


# Custom exception for the package config setup
class ConfigException(Exception):
    """System config exception class."""


def return_datadir() -> str | Path:
    """Return datadir based on the system install and config settings.

    Returns
    -------
    str | Path
        The current datadir directory
    """
    # Default is to use the local repo if this is an editable install
    if check_install_status() == "Editable":
        datadir = ROOT_DIR.parent
        return datadir
    # If fully installed (not editable), then use the user defined config
    elif check_install_status() == "Install":
        # Read the config file into the configparser object
        config.read(configfile)
        # Setting could be ~ so deal with it
        if config.get("DATADIR", "ROOT") == "~":
            datadir = Path("~").expanduser()
            return datadir
        # User may set their own directory (other than home)
        else:
            datadir = config.get("DATADIR", "ROOT")
            return datadir
    else:
        raise ConfigException("System config error: check system installation status.")

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_outputs() -> Path:
    """Return outputs directory path.

    Returns
    -------
    Path
        The current outputs directory
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the outputs subdirectory from the config file
    outputs = config.get("DATADIR", "OUTPUTS")
    outputs_path = Path(return_datadir()) / outputs
    return outputs_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_inputs() -> str | Path:
    """Return inputs directory path.

    Returns
    -------
    str | Path
        The current inputs directory
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the inputs subdirectory from the config file
    inputs = config.get("DATADIR", "INPUTS")
    inputs_path = Path(return_datadir()) / inputs
    return inputs_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_scratch() -> str | Path:
    """Return inputs directory path.

    Returns
    -------
    str | Path
        The current scratch directory
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the scratch subdirectory from the config file
    scratch = config.get("DATADIR", "SCRATCH")
    scratch_path = Path(return_datadir()) / scratch
    return scratch_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_logs_dir() -> Path:
    """Return the logs directory path from config.

    Returns
    -------
    Path
        The current logs directory
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the logs subdirectory from the config file
    logs_dir = config.get("LOGS", "PACKAGE_LOGS")
    logs_dir_path = Path(return_datadir()) / logs_dir
    return logs_dir_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_log_level() -> str:
    """Return the current log level.

    Returns
    -------
    str
        The current log level to define log output scope
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the config logs level from the config file
    log_level = config.get("LOGS", "LOG_LEVEL")
    return log_level

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def setup_directories(datadir_root_path: str | Path) -> None:
    """Create system directory structure.

    Parameters
    ----------
    str : Path
        Root of the datadir directory within which to create subdirectories
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get current subdirectories to create
    inputs_dir = return_inputs()
    outputs_dir = return_outputs()
    scratch_dir = return_scratch()
    logs_dir = return_logs_dir()
    # Ensure the datadir root is a path object
    datadir_path_obj = Path(datadir_root_path)
    # List subdirectories to be created
    subdirs_to_create = [inputs_dir, outputs_dir, scratch_dir, logs_dir]
    # Create subdirectories and parent dirs if required
    for subdir in subdirs_to_create:
        (datadir_path_obj / subdir).mkdir(parents=True, exist_ok=True)
    logger.info(f"Subdirectories created (or already exist): {subdirs_to_create}")
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


# TODO - consider change to take arg for debug level
# TODO - then set format level by debug type?
# Note - not linked directly to the config
def log_config(log_dir_path: Path) -> str | Path:
    """Log the system config settings to the config log file."""
    # Get full filepath to log files, using module constants
    log_for_config = log_dir_path / CONFIG_LOG_FILE
    log_for_system = log_dir_path / SYSTEM_LOG_FILE

    # Create config log file
    config_logger = create_config_logger(log_path=log_for_config)

    # Read the config file into the configparser object
    config.read(configfile)
    # Get the current user entered datadir root
    user_datadir = config.get("DATADIR", "ROOT")
    # Get key system config settings (depends on system install status)
    system_datadir = return_datadir()

    # Check current system install
    if check_install_status() == "Install":
        settings_message = f"Datadir root parsed: {system_datadir}"
    elif check_install_status() == "Editable":
        settings_message = "Editable install (see local within-repo log directory)"
    else:
        raise ConfigException("System config error: check system installation status.")

    # Write output to logfile
    config_logger.info(
        f"""
    -- System config --
    System installed as: {check_install_status(display=True)}
    Package dir: {PACKAGE_DIR}
    Config file datadir root, user setting is: {user_datadir}
    Settings: {settings_message}
        Config file datadir root (parsed) is: {return_datadir()}
        Outputs dir is: {return_outputs()}
        Inputs dir is: {return_inputs()}
        Scratch dir is: {return_scratch()}
        Logs dir is: {return_logs_dir()}
        Config logfile is: {log_for_config}
        System logfile is: {log_for_system}
    -- System config logged --
    """
    )
    return log_for_config


# TODO - add an issue to optimise and list logging performance issues


def main() -> None:
    """Process main config workflow."""
    # Read the config file into the configparser object
    config.read(configfile)
    # Get config settings from config.ini file
    datadir_input = config.get("DATADIR", "ROOT")
    # Parse the user settings and determine current specified path
    datadir_actual = return_datadir()

    # Create system directories
    # Required before logging starts so that the logs dir exists
    setup_directories(datadir_actual)

    # Setup system logging
    # Get full filepath to system log file, using module constant
    log_for_config = return_logs_dir() / SYSTEM_LOG_FILE
    # Create the system logger for both file and console output
    logger = create_system_logger(log_path=log_for_config)

    logger.info("  --- System logging started ---  ")

    if check_install_status() == "Install":
        logger.info(f"Config file datadir root user setting is: {datadir_input}")
    else:
        logger.info(
            "Config file datadir setting is IGNORED - editable install (see repo)"
        )
    logger.info(
        f"Config file datadir root (parsed),  is: {datadir_actual}, "
        f"dir exists: {Path(datadir_actual).is_dir()}"
    )

    # Log system settings to config log file under logs dir as set in config.ini
    log = log_config(return_logs_dir())
    logger.info(f"""Config logged at {log} """)

    # Note - called via CLI confirm-config, see setup.py
