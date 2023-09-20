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
from importlib.metadata import version

from simple.analysis.analysis import calculate
from simple.definitions import PACKAGE
from simple.netcdf.data import main

DEBUG = True
"""bool: Debugging level, module level constant (Default: True)."""

# Take the version number from the package version
pkg_version = version(PACKAGE)


def cli_entry_point(argv: list[str] | None = None) -> None:
    """Command line tool for the analysis calculate function.

    Parameters
    ----------
    argv : list[str]
           List of arguments supplied via the command line
           Default of none is used to trigger accepting supplied arguments from the
           command line when called via an entry point.

    Returns
    -------
    None
    """
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
    # Add optional version argument
    parser.add_argument(
        "--version",
        action="version",  # Prints version information and exits when invoked
        help="Display the version of the cli tool",
        version=f"{parser.prog} {pkg_version}",
    )
    # Run the parser and place the extracted data in an argparse.Namespace
    parsed_args = parser.parse_args(argv)

    # Run analysis calculation using the user provided input args
    result = calculate(parsed_args.x, parsed_args.y)

    print(result)  # print to stdout, don't return a value

    # Note cli tools may be expected to return none or 0 for testing
    # Note when developing cli tools, check for returncode if used and
    # compare use when called via function (no code) vs CLI tool (rtn code).

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            test_cli.py
    # b_integration     test_cli.py
    # c_end_to_end      test_cli.py
    # d_user_interface  test_cli.py
    # ===================================================================


def cli_data(argv: list[str] | None = None) -> None:
    """Command line tool for data creation, with options.

    Parameters
    ----------
    argv : list[str]
           List of arguments supplied via the command line
           Default of none is used to trigger accepting supplied arguments from the
           command line when called via an entry point.

    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser(
        prog="CREATE-DATA",
        description="Create data files in datadir.",
        epilog="  ---  ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Arguments in argparse can be positional or optional
    # The optional args are prefixed by - or --
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print progress and data info to stdout",
    )
    parser.add_argument(
        "--version",
        action="version",  # Prints version information and exits when invoked.
        help="Display the version of the cli tool",
        version=f"{parser.prog} {pkg_version}",
    )
    parser.add_argument(
        "value", type=int, help="Value within netcdf", choices=[0, 1, 2, 3, 4, 5]
    )
    # parse to namespace object
    parsed_args = parser.parse_args(argv)
    # TODO add use of value
    # Run using the user provided input args
    main(debug=parsed_args.verbose)
    # Note cli tools may be expected to return none or 0 for testing
    # When developing tests for cli tools, check the use of returncode

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            test_cli.py
    # b_integration     test_cli.py
    # c_end_to_end      test_cli.py
    # d_user_interface  test_cli.py
    # ===================================================================
