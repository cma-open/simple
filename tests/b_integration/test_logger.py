"""Tests for the logging module."""
import logging

from simple.config.reader import return_verbosity


def test_available_logger():
    """Test the wider system to check selected expected loggers are present."""
    # Get all logger objects
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    # Convert to list of strings
    loggers_names = [str(logger) for logger in loggers]
    expected_loggers = [
        "<Logger simple (DEBUG)>",
        "<Logger ConfigLog (DEBUG)>",
        # "<Logger DEMOLog (DEBUG)>",
    ]
    # Print full list of logggers for verbose editable installs
    if return_verbosity():
        print(*loggers, sep="\n")
        print("---")
    # Check that the selected list of expected loggers are present
    for logger in expected_loggers:
        assert logger in loggers_names

    # TODO - see issue #46
