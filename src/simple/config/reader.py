"""Reader module for system config ini file."""

import configparser
import logging
import os
from pathlib import Path

from simple.common.common import check_install_status
from simple.definitions import PACKAGE_DIR

config = configparser.ConfigParser()

# Set path to user edited config file
configfile = f"{PACKAGE_DIR}/config.ini"
# Not supplied with docstring so filepath is not visible in sphinx docs

# def read_input_source_ini(self):
#     """Read input sources from the ini config file."""
#
#     # read the config file into the configparser object
#     config.read(configfile)
#
#     if self.service == "COP":
#         if self.dataset == "E-OBS":
#             self.long = config.get("COP", "COP_DATASET")
#
#         self.format = config.get("COP", "COP_FORMAT")
#         self.product_type = config.get("COP", "COP_PRODUCT_TYPE")
#         self.variables = config.get("COP", "COP_VARIABLES")
#         self.grid_res = config.get(("COP"), "COP_GRID_RES")
#         self.period = config.get("COP", "COP_PERIOD")
#         self.version = config.get("COP", "COP_VERSION")


def read_ini():
    """Read input sources from the ini config file."""
    # read the config file into the configparser object
    config.read(configfile)

    # main default is to use the local repo if this is an editable install
    if check_install_status() == "Editable":
        datadir = os.path.dirname(os.path.dirname(PACKAGE_DIR))
        return datadir
    # if installed as a user, then use the user defined config
    else:
        # setting could be ~ so deal with it
        if config.get("DATADIR", "ROOT") == "~":
            datadir = Path("~").expanduser()
            return datadir
        # user may set their own directory
        else:
            datadir = config.get("DATADIR", "ROOT")
            return datadir


def return_outputs():
    """Return outputs directory path."""
    # read the config file into the configparser object.
    config.read(configfile)
    outputs = config.get("DATADIR", "OUTPUTS")
    outputs_path = Path(read_ini()) / outputs
    return outputs_path


def validate_dir(dir_path):
    """Validate directory paths."""
    pass


def setup_directories(dir_path):
    """Create system directory structure."""
    # read the config file into the configparser object.
    config.read(configfile)
    # get subdirs to create
    inputs_dir = config.get("DATADIR", "INPUTS")
    outputs_dir = config.get("DATADIR", "OUTPUTS")
    (Path(dir_path) / inputs_dir).mkdir(parents=True, exist_ok=True)
    (Path(dir_path) / outputs_dir).mkdir(parents=True, exist_ok=True)
    (Path(dir_path) / "logs").mkdir(parents=True, exist_ok=True)


def log_config(dir_path):
    """Log system config settings to the config log file."""
    # read the config file into the configparser object.
    config.read(configfile)
    # create log filename
    log_for_config = Path(dir_path) / config.get("LOGS", "CONFIG")
    # Set format for log message construction
    log_format = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(
        filename=log_for_config,
        encoding="utf-8",
        filemode="w",
        format=log_format,
        level=logging.DEBUG,
    )
    # log key system config settings to file
    user_datadir = config.get("DATADIR", "ROOT")
    if check_install_status() == "User":
        settings_message = f"datadir root parsed: {dir}"
    else:
        settings_message = (
            "Config file datadir setting is IGNORED, as editable install (see repo)"
        )
    logging.debug("  -- System config -- ")
    logging.info(
        f"""
    System installed as: {check_install_status(display=True)}
    Package dir: {PACKAGE_DIR}
    Config datadir root, user setting is: {user_datadir}
    Settings: {settings_message}
        Datadir is: {dir}/data
    """
    )
    return log_for_config


def main():
    """Process main config workflow."""
    # read the config file into the configparser object
    config.read(configfile)
    # Get config settings
    datadir_input = config.get("DATADIR", "ROOT")
    datadir_actual = read_ini()  # parse the user setting and determine path
    # Print out config settings to terminal
    print("    ----  config  ----    ")
    print(f"Config file: {configfile}")
    if check_install_status() == "User":
        print(f"Config datadir root user setting is: {datadir_input}")
    else:
        print("Config file datadir setting is IGNORED, as editable install (see repo)")
    print(
        f"Datadir root, parsed,  is: {datadir_actual}, "
        f"dir exists: {Path(datadir_actual).is_dir()}"
    )
    print(f"Datadir is: {datadir_actual}/data")
    setup_directories(datadir_actual)
    log = log_config(datadir_actual)
    print(f"Config logged at {log}")
    print("    ---- end config setup ----")
    print()
