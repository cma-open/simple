"""Setup system directories and loggers."""

import logging
from pathlib import Path

from simple.common.common import check_install_status, debug_loggers
from simple.config.reader import (
    ConfigException,
    return_datadir,
    return_datadir_root,
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


def setup_directories(datadir_root_path: str | Path) -> None:
    """Create system directory structure.

    Parameters
    ----------
    str : Path
        Root of the datadir directory within which to create subdirectories
    """
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

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            setup/test_system_setup.py
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
    # Create required system directory structure
    logger_name.debug("Creating directories")
    setup_directories(datadir_root_path=return_datadir())

    # Update system log with added log file handler
    # (Log already exists via init)
    update_system_log(logger=system_logger)
    logger_name.debug("System directories created")

    # Log the system configuration to file
    # Log system settings to config log file under logs dir as set in config.ini
    log_config(return_logs_dir())
    logger_name.info(f"Config logged to file in {return_logs_dir()}")
    logger_name.info(f"System log file created in {return_logs_dir()}")
    logger_name.debug(f"System log: {logger_name}")
    logger_name.info("System setup has run")

    # Print out current loggers - only for editable installs
    if check_install_status() == "Editable":
        debug_loggers()
