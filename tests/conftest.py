"""Pytest config extensions to supplement standard test report output.

Functions help to catch situations where tests are run before the package
has been installed.
"""

import pytest

from simple.common.common import check_install_status


def pytest_report_header(config):
    """Add text information to test report header."""
    return [
        "Extra info: example",
        f"Tests run from install type: {check_install_status()}",
    ]


def pytest_collectreport(report):
    """Raise pytest error if test report fails."""
    if report.failed:

        raise pytest.UsageError(
            "- \n"
            "Errors during collection \n"
            "Check package has been installed correctly \n"
            "Have you run 'pip install .' or 'pip install -e .' ? \n"
            "Aborting tests"
            " \n"
        )
