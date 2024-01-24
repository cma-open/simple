"""Reader module for system config ini file."""

import configparser
import logging
import os
from pathlib import Path

from simple.common.common import check_install_status
from simple.definitions import PACKAGE_DIR, RESOURCES_DIR, ROOT_DIR
from simple.logger.log import CONFIG_LOG_FILE, SYSTEM_LOG_FILE, create_config_logger

# Set module level logger
logger = logging.getLogger(__name__)

# Create configparser object
config = configparser.ConfigParser()
# Allow for testing system use via GitHub action  with test config
# Otherwise use set path to user edited config file
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
if IN_GITHUB_ACTIONS:
    configfile = RESOURCES_DIR / "github_config.ini"
else:
    configfile = f"{PACKAGE_DIR}/config.ini"
# Not supplied with docstring so filepath is not visible in sphinx docs

# Add note here and link to the package system strategy for logging
# e.g. log output, file vs. terminal, module level etc.


# Custom exception for the package config setup
class ConfigException(Exception):
    """System config exception class."""


def return_datadir() -> str | Path:  # TODO
    """Return datadir based on the system install and config settings.

    Returns
    -------
    str | Path
        The current datadir directory
    """
    # Default is to use the local repo if this is an editable install
    if check_install_status() == "Editable":
        datadir = ROOT_DIR.parent
        return Path(datadir)
    # If fully installed (not editable), then use the user defined config
    elif check_install_status() == "Install":
        # Read the config file into the configparser object
        config.read(configfile)
        # Setting could be ~ so deal with it
        if config.get("DATADIR", "ROOT") == "~":
            datadir = Path("~").expanduser()
            return datadir
        # Setting could be a subdir within ~
        elif "~" in config.get("DATADIR", "ROOT"):
            datadir = Path(config.get("DATADIR", "ROOT")).expanduser()
            return datadir
        # User may set their own directory (other than home)
        else:
            datadir = config.get("DATADIR", "ROOT")
            return Path(datadir)
    else:
        raise ConfigException("System config error: check system installation status.")
    # TODO add call to logger here to capture exception

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
        The current outputs directory as a full path
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the outputs subdirectory from the config file
    outputs = config.get("DATADIR", "OUTPUTS")
    outputs_path = Path(return_datadir()) / outputs
    if return_verbosity():
        logger.debug(f"Outputs: {outputs_path}")
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
        The current inputs directory as a full path
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the inputs subdirectory from the config file
    inputs = config.get("DATADIR", "INPUTS")
    inputs_path = Path(return_datadir()) / inputs
    if return_verbosity():
        logger.debug(f"Inputs: {inputs_path}")
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
        The current scratch directory as a full path
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the scratch subdirectory from the config file
    scratch = config.get("DATADIR", "SCRATCH")
    scratch_path = Path(return_datadir()) / scratch
    if return_verbosity():
        logger.debug(f"Scratch: {scratch_path}")
    return scratch_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     test_config_reader.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_demo_temp() -> Path:
    """Return demo_temp directory path.

    Returns
    -------
    Path
        The demo_temp directory as a full path
    """
    demo_temp_path = Path(return_datadir()) / "demo_temp"
    if return_verbosity():
        logger.debug(f"Demo_temp: {demo_temp_path}")
    return demo_temp_path

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py TODO
    # b_integration     test_config_reader.py TODO
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_logs_dir() -> Path:
    """Return the logs directory path from config.

    Returns
    -------
    Path
        The current logs directory as a full path
    """
    # Read the config file into the configparser object.
    config.read(configfile)
    # Get the current setting for the logs subdirectory from the config file
    logs_dir = config.get("LOGS", "PACKAGE_LOGS")
    logs_dir_path = Path(return_datadir()) / logs_dir
    if return_verbosity():
        logger.debug(f"Logs path: {logs_dir_path}")
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
    if return_verbosity():
        logger.debug(f"Log level: {log_level}")
    return log_level

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            config/test_reader.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def return_datadir_root() -> str | Path:
    """Return datadir root user value.

    Returns
    -------
    str | Path
        The datadir root directory
    """
    # Read the config file into the configparser object
    config.read(configfile)
    # Get the current user entered datadir root
    user_datadir = config.get("DATADIR", "ROOT")
    return user_datadir


def return_verbosity() -> bool:
    """Return log verbosity setting for editable installs.

    Returns
    -------
    str | Path
        The log verbosity setting
    """
    # Read the config file into the configparser object
    config.read(configfile)
    # Get the current user entered setting
    verbosity_setting = config.get("LOGS", "VERBOSE")
    if verbosity_setting in ["true", "True"] and check_install_status() == "Editable":
        verbosity = True
    else:
        verbosity = False
    return verbosity


# TODO add tests


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
        demo_temp dir is: {return_demo_temp()}
        Config logfile is: {log_for_config}
        System logfile is: {log_for_system}
        Log level: {return_log_level()}
        Log verbosity: {return_verbosity()}
    -- System config logged --
    """
    )
    return log_for_config


# TODO - add an issue to optimise and list logging performance issues
