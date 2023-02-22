"""Command line tool - a simple analysis tool example.

Takes user supplied parameters and conducts analysis, prints output to terminal.

Example
-------
Example text here including
literal blocks::
    $ python cli.py
"""
# TODO replace above example

import argparse

import pkg_resources

from simple.analysis.analysis import calculate
from simple.definitions import PACKAGE
from simple.netcdf.data import main

DEBUG = True
"""bool: Debugging level, module level constant (Default: True)."""

# Take the version number from the package version in setup
pkg_version = pkg_resources.get_distribution(PACKAGE).version


def cli_entry_point(argv=None):
    """Command line tool for analysis calculate function."""
    parser = argparse.ArgumentParser(
        prog="CLI-SIMPLE",
        description="A simple app to conduct analysis on two integers",
        epilog="  ---  ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Arguments in argparse can be positional or optional
    # Set the argument type and limit choices from a list
    # Note type is set to int, to force conversion
    parser.add_argument("x", type=int, help="the x value", choices=[0, 1, 2, 3, 4, 5])
    parser.add_argument("y", type=int, help="the y value", choices=[0, 1, 2, 3, 4, 5])
    parser.add_argument(
        "--version",
        action="version",  # Prints version information and exits when invoked
        help="Display the version of the cli tool",
        version=f"{parser.prog} {pkg_version}",
    )
    parsed_args = parser.parse_args(argv)
    # run analysis calculation using the user provided input args
    result = calculate(parsed_args.x, parsed_args.y)
    print(result)  # print to stdout, don't return value
    # Note cli tools may be expected to return none or 0 for testing
    # When developing tests for cli tools, check the use of returncode


def cli_data(argv=None):
    """Command line tool for data creation, with options."""
    parser = argparse.ArgumentParser(
        prog="CREATE-DATA",
        description="Create data files in datadir.",
        epilog="  ---  ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Arguments in argparse can be positional or optional
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress and data info to stdout"
    )
    parser.add_argument(
        "--version",
        action="version",  # Prints version information and exits when invoked
        help="Display the version of the cli tool",
        version=f"{parser.prog} {pkg_version}",
    )
    parsed_args = parser.parse_args(argv)
    # run using the user provided input args
    main(debug=parsed_args.verbose)
    # Note cli tools may be expected to return none or 0 for testing
    # When developing tests for cli tools, check the use of returncode
