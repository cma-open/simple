"""System status and performance checks and reports."""

import logging
from importlib.metadata import version

from simple.common.common import check_install_status
from simple.config.reader import (
    ConfigException,
    return_datadir,
    return_datadir_root,
    return_inputs,
    return_log_level,
    return_logs_dir,
    return_outputs,
    return_scratch,
    return_verbosity,
)
from simple.definitions import PACKAGE, PACKAGE_DIR
from simple.logger.log import CONFIG_LOG_FILE, SYSTEM_LOG_FILE

logger = logging.getLogger(__name__)


def show_version():
    """Show current system package version to terminal and log."""
    system_version = version(PACKAGE)
    logger.info(f"System version: {PACKAGE}-{system_version}")


def confirm_config() -> None:
    """Process main config and print to terminal."""
    # This function largely replicates the function system_setup.log_config
    # however nothing is logged, only printed to terminal

    # Parse the user settings and determine current specified path
    # (depends on system install status)
    actual_system_datadir = return_datadir()
    # Get logs directories from config
    logs_dir = return_logs_dir()
    # Get full paths to subdirs
    log_dir_path = actual_system_datadir / logs_dir
    # Get full filepath to log files, using module constants
    log_for_config = log_dir_path / CONFIG_LOG_FILE
    # Not at this point system log may not yet have been created
    # this highlights to the user where it can be found later
    log_for_system = log_dir_path / SYSTEM_LOG_FILE
    # Get the user entered datadir root
    user_datadir = return_datadir_root()
    # Check current system install
    if check_install_status() == "Install":
        settings_message = f"Datadir root parsed: {actual_system_datadir}"
    elif check_install_status() == "Editable":
        settings_message = (
            "Editable install "
            "(see local within-repo directory, user setting is ignored)"
        )
    else:
        raise ConfigException("System config error: check system installation status.")

    # Print output to terminal
    print(
        f"""
     --  config --
     System installed as: {check_install_status()}
     Package dir: {PACKAGE_DIR}
     Package name: {PACKAGE}
     Package/system version: {version(PACKAGE)}
     Settings: {settings_message}
         Config file datadir root, user setting is: {user_datadir}
         Config file datadir root (parsed) is: {return_datadir()}
         Outputs dir is: {return_outputs()}
         Inputs dir is: {return_inputs()}
         Scratch dir is: {return_scratch()}
         Logs dir is: {return_logs_dir()}
         Config logfile is: {log_for_config}
         System logfile is: {log_for_system}
         Log level: {return_log_level()}
         Log verbosity: {return_verbosity()}
     --  config --
     """
    )
    logger.debug("Confirm-config ran.")
