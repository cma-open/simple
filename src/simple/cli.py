"""Command line application - a simple analysis tool example.

Example
-------
Example text here including
literal blocks::
    $ python cli.py
"""

import argparse

import pkg_resources

from simple.analysis.analysis import calculate
from simple.definitions import PACKAGE

DEBUG = True
"""bool: Debugging level, module level constant (Default: True)."""

# Take the version number from the package version in setup
pkg_version = pkg_resources.get_distribution(PACKAGE).version


def cli_entry_point(argv=None):
    """CLI tool, pass command line arguments to the analysis calculate function."""
    parser = argparse.ArgumentParser(
        prog="CLI-SIMPLE",
        description="A simple app to conduct analysis on two integers",
        epilog="  ---  ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Arguments in argparse can be positional or optional
    # Set the argument type and limit choices from a list

    parser.add_argument("x", type=int, help="the x value", choices=[0, 1, 2, 3, 4, 5])
    parser.add_argument("y", type=int, help="the y value", choices=[0, 1, 2, 3, 4, 5])

    parser.add_argument(
        "--version",
        action="version",  # Prints version information and exits when invoked
        help="Display the version of the cli tool",
        version=f"{parser.prog} {pkg_version}",
    )

    parsed_args = parser.parse_args(argv)

    # run analysis
    x = parsed_args.x
    y = parsed_args.y

    result = calculate(x, y)
    print(f"Result: {result}")
    return result
