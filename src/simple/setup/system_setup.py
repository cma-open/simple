"""Setup system directories and loggers."""

import datetime
import json
import logging
import os
from importlib.metadata import metadata, version
from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir, user_data_dir, user_log_dir

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

# note - system_logger exist and logs all INFO level and above to console (not DEBUG)

# CONTENTS - temp dev notes
# key_directories - list key directories from config
# verify_directories - check if all key directories exit
# setup_directories - create key directories on disk
# log_config - logs system config to a log file on disk (path set in config file)
#    config.log
# setup_system_log - setup main system log file, as set by config file
#    system.log
#    DEBUG level and above go to file
# update_system_log - takes system log by name and adds a log file handler (system.log)
# system_setup - checks system status and creates dirs and logs if required
#    acts differently on initial setup vs changed system config status
#    possible states are: new setup (no dirs, no logs), amended config (dirs, logs_
#    checks if system directories exist (verify_directories), creates if not
#    logs to main system console log to inform user if creating directories
#    updates main system log by name "simple" to add the file handler (system.log)
#    note - append status   note - no impact if already exists?
#    runs log_config to log config to file (config.log) (new file every time)
#    several messages at DEBUG level to file to log system_steup has run

# options
# add further status checks within system_setup
# once system has been installed then config file wil exist?
# check if config log exist, check if it has changed if it does


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
        # TODO check re remove prints
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


def read_config_log(file_path):
    """
    Read the contents of the config log file.

    Parameters
    ----------
    file_path : str
        The path to the config log file.

    Returns
    -------
    str or None
        The contents of the config log file, or None if the file does not exist.
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as file:
        return file.read()


def normalize_indentation(data):
    """
    Normalize the indentation of the data by removing leading whitespace from each line.

    Parameters
    ----------
    data : str
        The data to normalize.

    Returns
    -------
    str
        The normalized data.
    """
    lines = data.split("\n")
    normalized_lines = [line.lstrip() for line in lines]
    return "\n".join(normalized_lines).strip()


def compare_data(old_data, new_data):
    """
    Compare old data with new data.

    Normalizing indentation and ignoring the first line (datetime stamp)
    in the old data.

    Parameters
    ----------
    old_data : str
        The old data to compare.
    new_data : str
        The new data to compare.

    Returns
    -------
    bool
        True if the data is different, False otherwise.
    """
    # Split the old data into lines and ignore the first line (datetime stamp)
    old_data_lines = old_data.strip().split("\n")[1:]
    new_data_lines = new_data.strip().split("\n")
    # Normalize indentation
    old_data_normalized = normalize_indentation("\n".join(old_data_lines))
    new_data_normalized = normalize_indentation("\n".join(new_data_lines))
    return old_data_normalized != new_data_normalized


def check_config_log(log_dir_path: Path):
    """
    Check if the config log file needs to be updated.

    Parameters
    ----------
    log_dir_path : Path
        The directory path where the log files are stored.

    Returns
    -------
    bool
        True if the config log file needs to be updated, False otherwise.
    """
    log_for_config = log_dir_path / CONFIG_LOG_FILE
    old_data = read_config_log(log_for_config)
    new_data = generate_log_content(log_dir_path)

    if old_data is None:
        logger_name.info("Config log does not exist. New data will be written.")
        return True

    if compare_data(old_data, new_data):
        logger_name.info("Config settings have changed. New data will be written.")
        return True
    else:
        # Data has not changed. No need to update the log.
        # No output to the user or to the logs
        return False


def generate_log_content(log_dir_path: Path) -> str:
    """
    Generate the config log content as a string.

    Parameters
    ----------
    log_dir_path : Path
        The directory path where the log files are stored.

    Returns
    -------
    str
        The config log content as a string.
    """
    # Get full filepath to log files, using module constants
    log_for_config = log_dir_path / CONFIG_LOG_FILE
    log_for_system = log_dir_path / SYSTEM_LOG_FILE
    # Get the current user entered datadir root
    user_datadir = return_datadir_root()
    # Get key system config settings (depends on system install status)
    system_datadir = return_datadir()
    if check_install_status() == "Install":
        settings_message = f"Datadir root parsed: {system_datadir}"
    elif check_install_status() == "Editable":
        settings_message = "Editable install (see local within-repo log directory)"
    else:
        raise ConfigException("System config error: check system installation status.")

    log_content = f"""
    --  config --
    System installed as: {check_install_status(display=True)}
    Package dir: {PACKAGE_DIR}
    System version: {PACKAGE}-{version(PACKAGE)}
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
    return log_content


# TODO - consider change to take arg for debug level
# TODO - then set format level by debug type?
# Note - not linked directly to the config
def log_config(log_dir_path: Path) -> str | Path:
    """
    Log the system config settings to the config log file.

    Parameters
    ----------
    log_dir_path : Path
        The directory path where the log files are stored.

    Returns
    -------
    str or Path
        The path to the config log file.
    """
    # Get full filepath to log files, using module constants
    log_for_config = log_dir_path / CONFIG_LOG_FILE
    # Create the config logger
    config_logger = create_config_logger(log_path=log_for_config)
    # get the content from the config settings
    log_content = generate_log_content(log_dir_path)
    # Write content as a log message
    config_logger.info(log_content)
    logger_name.info(f"Config log created or updated at: {log_for_config}")
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
    # Main package logger always exists because it is created in init
    # This just adds the system log file handler and formatter
    # Send messages DEBUG and above to system.log
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
    # START

    # Set log_dir_path from config settings (config.ini)
    log_dir_path = return_logs_dir()
    # Log system settings to config log file under logs dir as set in config.ini
    # Only update log if the config settings have changed.
    if check_config_log(log_dir_path):
        log_config(log_dir_path)

    # Check and move log messages within the main functions to manage log outputs
    # Log messages will be frequently called, therefore set to debug, for file

    # LOGGING NOTE
    # Important logs occur within the called contained functions
    # This function has different impact when run in a new installation.
    # Because constantyl called in init, no log messages in this function.

    # logger_name.debug(f"System log file created or updated in {return_logs_dir()}")
    # logger_name.debug(f"System log: {logger_name}")
    # logger_name.debug("System setup has run")


def get_user_data_dir():
    """Get user data dir."""
    appname = "MyPackage"
    appauthor = "MyCompany"
    return user_data_dir(appname, appauthor)


def write_installation_log(version):
    """Write details to installation log file."""
    data_dir = get_user_data_dir()
    os.makedirs(data_dir, exist_ok=True)
    log_file = os.path.join(data_dir, "install_log.json")

    log_data = {
        "installed_version": version,
        "install_time": datetime.datetime.now().isoformat(),
        "install_log": str(log_file),
        "System installed as": check_install_status(display=True),
        "Package dir": str(PACKAGE_DIR),
    }

    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        try:
            with open(log_file, "r") as f:
                existing_data = json.load(f)
            log_data["previous_version"] = existing_data.get("installed_version")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading existing log file: {e}")

    try:
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=4)
    except IOError as e:
        print(f"Error writing log file: {e}")


def print_installation_log():
    """Print installation log content to terminal."""
    data_dir = get_user_data_dir()
    log_file = os.path.join(data_dir, "install_log.json")

    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        try:
            with open(log_file, "r") as f:
                log_data = json.load(f)
            print(json.dumps(log_data, indent=4))
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading log file: {e}")
    else:
        print("Log file does not exist or is empty.")


def get_platformdirs():
    """Get platformdirs paths."""
    appname = PACKAGE
    appauthor = metadata(PACKAGE)["Author"]
    print(user_data_dir(appname, appauthor))
    print(user_cache_dir(appname, appauthor))
    print(user_config_dir(appname, appauthor))
    print(user_log_dir(appname, appauthor))


if __name__ == "__main__":
    get_platformdirs()
    package_version = version(PACKAGE)
    write_installation_log(package_version)
    print_installation_log()

# start
# options
# copy config to setup
# ensure localy write f last version installed and current version
# also previous log path vs current log path
# then check those ans trigger re setup

# other quick way to amend system_setup()
# change so that only runs if log file in those locations dotn exist,
# otherwide use them
# think through re config though,
# consider using checksum or similar to compare content of eg config.log
# to check if it changed?

# also re-visit and update section on loging methods
# do a quick web search and state how logs sit with the functinos where
# they are enacted and only limited
# additional logs in the "calling" scripts to ensure thye are easy to test,
# mock and manage
# e.g. log at thr gith place, so within functinos
# wrapper or calling fucntino just log the approx start, or process flow,
# or end of a workflow
