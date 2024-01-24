"""Setup system directories and loggers."""

import logging
from pathlib import Path

from simple.common.common import check_install_status
from simple.config.reader import (
    ConfigException,
    return_datadir,
    return_datadir_root,
    return_demo_temp,
    return_inputs,
    return_logs_dir,
    return_outputs,
    return_scratch,
)
from simple.definitions import PACKAGE, PACKAGE_DIR
from simple.logger.log import (
    CONFIG_LOG_FILE,
    SYSTEM_LOG_FILE,
    add_system_log_file_handler,
    create_config_logger,
    create_system_logger,
)

# Get logger name via module name
logger_name = logging.getLogger(__name__)
# Get system logger via package name - already exists via init
system_logger = logging.getLogger(PACKAGE)


def key_directories() -> list:
    """Key system directories list.

    Returns
    -------
    list
        List of the main system directories, full paths
    """
    key_directories = [
        return_inputs(),
        return_outputs(),
        return_scratch(),
        return_demo_temp(),
        return_logs_dir(),
    ]
    return key_directories


# ToDo move to common or status if it is needed elsewhere in system
def verify_directories() -> bool:
    """Verify required directories exist.

    Returns
    -------
    bool
        True if all required directories exist on disk.
    """
    # List subdirectories to be created
    subdirs_to_create = key_directories()
    # Set list to collect responses
    dir_exists = []
    # Check if subdirectories exist
    for subdir in subdirs_to_create:
        dir_exists.append(subdir.is_dir())
    # Convert to single value (True if all dirs exist, otherwise False)
    dirs_all_exist = all(dir_exists)
    return dirs_all_exist

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            ?
    # b_integration     ?
    # c_end_to_end      ?
    # d_user_interface  ?
    # ===================================================================


def setup_directories(key_directories: list) -> None:
    """Create system directory structure.

    Parameters
    ----------
    str : key_directories
        List of main directories to be created for the system
    """
    # Create subdirectories and parent dirs if required
    print(f"key directories: {key_directories}")
    for subdir in key_directories:
        print(subdir)
        # (datadir_path_obj / subdir).mkdir(parents=True, exist_ok=True) TODO
        subdir.mkdir(parents=True, exist_ok=True)

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            setup/test_system_setup.py TODO check and refactor
    # b_integration     N/A TODO >>>>>>>>
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
    # Although at this point system log is not yet created
    # this highlights to the user where it can be found later
    log_for_system = log_dir_path / SYSTEM_LOG_FILE
    # Create config log file
    config_logger = create_config_logger(log_path=log_for_config)
    # Get the current user entered datadir root
    user_datadir = return_datadir_root()
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
    --  config --
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
    --  config logged --
    """
    )
    return log_for_config

    # TODO - tests table


def setup_system_log() -> None:
    """Create the main system logger."""
    # Get full filepath to system log file, using module constant
    # add try except to catch if dir does not exist yet
    try:
        system_log_path = return_logs_dir() / SYSTEM_LOG_FILE
        logger = create_system_logger(system_log_path)
        return logger
    except FileNotFoundError:
        raise FileNotFoundError(
            "System setup must be run before system use (See User Instructions)"
        )

    # TODO test table


def update_system_log(logger: str) -> None:
    """Update existing system logger with log file."""
    # Main package logger always exists because created in init
    # This just adds the file formatter
    system_log_path = return_logs_dir() / SYSTEM_LOG_FILE
    add_system_log_file_handler(logger=logger, log_path=system_log_path)

    # TODO test table


def system_setup() -> None:
    """System setup of directories and loggers."""
    # Initially only the package level system logger exists (system_logger)
    # if not verify_directories(datadir_root_path=return_datadir()): TODO
    if not verify_directories():
        # Log to terminal and file as relatively infrequent occurrence
        system_logger.info("Some required dirs don't exist on disk")
        system_logger.info("Creating required directories")
        system_logger.info("System setup running")
        setup_directories(key_directories=key_directories())

    # Update system log with added log file handler
    # (Log already exists via init)
    update_system_log(logger=system_logger)

    # Log system settings to config log file under logs dir as set in config.ini
    log_config(return_logs_dir())
    # Log messages will be frequently called, therefore set to debug, for file
    logger_name.debug(f"Config logged to file in {return_logs_dir()}")
    logger_name.debug(f"System log file created or updated in {return_logs_dir()}")
    logger_name.debug(f"System log: {logger_name}")
    logger_name.debug("System setup has run")
