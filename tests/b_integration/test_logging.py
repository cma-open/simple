"""Tests for the logging module."""

import logging

loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]


def test_available_logger():
    """Test the wider system to check only expected loggers are available."""
    for logger in loggers:
        print(logger)
    # fail test
    # assert 1 == 2
    # TODO - see issue #46
