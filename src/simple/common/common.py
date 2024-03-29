"""Common system functions."""

import logging
from importlib.util import find_spec
from pathlib import Path

from simple.definitions import PACKAGE

# Set logger
logger = logging.getLogger(__name__)

# Do not use setup system logger here


class StatusException(Exception):
    """System install status exception class."""


def check_install_status(display=None) -> str:
    """Check if system is installed as full or editable develop install.

    Returns
    -------
    str
        String indicating current system installation status

    """
    # Note - designed for a src package structure
    spec = find_spec(PACKAGE)
    test_source = "src" in spec.origin
    test_site_packages = "site-packages" in spec.origin
    if test_source:
        # TODO check and fix use of display
        # if display:
        # logger.info(f"Editable install XXXXXXX at: {spec.origin}")
        return "Editable"
    elif test_site_packages:
        # if display:
        # logger.info(f"Full install into site-packages at: {spec.origin}")
        return "Install"
    else:
        raise StatusException("System status error: Unknown path or not installed")
        # TODO log error

    # change to raise error and then capture in logs

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            common/test_common.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def clean_directory(dir_path: str | Path, files: list) -> None:
    """Remove specified list of files from named directory.

    Parameters
    ----------
    dir_path : str | Path
        Directory within which to remove files
    files : list
        List of filenames to be removed (as strings)
    """
    for file in files:
        filepath = Path(dir_path) / file
        # Remove this file or symbolic link
        filepath.unlink(missing_ok=True)
        logger.debug(f"Removed: {filepath} ")

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            common/test_common.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def debug_loggers() -> None:
    """Print current available logger names and associated handlers."""
    # Used for dev debugging, kept for potn future use
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    print("--------------------------------------------------")
    for logger in loggers:
        print(logger, logger.handlers)
    print("--------------------------------------------------")
