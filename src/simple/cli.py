"""Command line tools.

Example
-------
Example text here including
literal blocks::
    $ python cli.py
"""
# TODO replace above example

import argparse
import logging
import sys
from importlib.metadata import version
from pathlib import Path

from simple.analysis.analysis import calculate
from simple.definitions import PACKAGE
from simple.demos.demos import demo_logs
from simple.netcdf.data import main

# Take the version number from the package version
pkg_version = version(PACKAGE)

# Note - reminder (keep) no need to setup logging
# Already instantiated logger

# Set module logger
logger = logging.getLogger(__name__)

# Purpose
# These commands mainly use argparse to manage user input, options and feedback
# Other simple commands that do not use argparse are located in their parent modules.

# Contents
# cli_entry_point (command = cli-simple)
# cli_data   (command = create-data-options)
# demo_logs_cli_entry_point (command = cli-demo-logs
# demo_logs_main (command = demo-logs)  (no argparse)


def cli_entry_point(argv: list[str] | None = None) -> None:
    """Command line tool for the analysis calculate function.

    Parameters
    ----------
    argv : list[str] | None
           List of arguments supplied via the command line
           Default of none is used to trigger accepting supplied arguments from the
           command line when called via an entry point.
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
    # Log that the cli tool is running, with inputs
    logger.debug(
        f"Running cli-simple tool with - x: {parsed_args.x}, " f"y: {parsed_args.y}, "
    )
    print(result)  # print to stdout, don't return a value
    logger.debug(f"cli-simple tool result: {result}")
    logger.info("cli-simple tool has run.")

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
    logger.debug(f"Running: {parser.prog}")
    logger.debug(f"Value(s): {parsed_args.value}")
    logger.debug(f"Verbose: {parsed_args.verbose}")
    # Run using the user provided input args
    main(debug=parsed_args.verbose)
    logger.info("Tool has run.")
    logger.info(f"Tool {parser.prog} has run.")
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


def demo_logs_cli_entry_point(argv: list[str] | None = None) -> None:
    """Argparse wrapped function to call demo logs.

    Parameters
    ----------
    argv : list[str] | None
           List of arguments supplied via the command line
           Default of none is used to trigger accepting supplied arguments from the
           command line when called via an entry point.
    """
    # Used by command cli-demo-logs (see pyproject.toml)
    # This shows additional functionality of argparse
    # Also shows additional testing potential
    # Illustrates a dry-run option

    parser = argparse.ArgumentParser(
        prog="CLI-DEMO-LOGS",
        description="A command line tool to demo logs.\n"
        "If no directory is supplied then files will be written into a \n"
        "directory 'demo_temp' within DATADIR.",
        epilog="  ---  ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # Arguments in argparse can be positional or optional
    # Set the argument type and limit choices from a list
    parser.add_argument(
        "demo_log_dir", help="Directory to write demo logs to", default=None, nargs="?"
    )
    # nargs ? single value, but optional
    # Therefore command can be run with no arguments supplied.

    parser.add_argument(
        "-d",
        "--dry",
        action="store_true",
        help="Run the command without enacting full functionality",
    )

    try:
        # Run the parser and place the extracted data in an argparse.Namespace
        parsed_args = parser.parse_args(argv)
        # TODO remove
        print(f"parsed args: {parsed_args}")

        # dry run option just logs a message, no demo logs are created
        if parsed_args.dry:
            logger.debug(f"{parser.prog} command run in dry-run mode. Exiting")

        else:
            # For any set demo_temp paths, ensure Path object
            if parsed_args.demo_log_dir:
                # Convert back to a path object
                demo_log_dir_path = Path(parsed_args.demo_log_dir)
                parent_directory = demo_log_dir_path.parent
                if parent_directory.exists() and parent_directory.is_dir():
                    logger.debug(
                        f"Running cli-demo-logs tool with custom dir: "
                        f"{demo_log_dir_path}"
                    )
                else:
                    raise FileNotFoundError(
                        f"Parent directory does not exist: {parent_directory}"
                    )
            else:
                # If no custom path set, then set as None and let demo_logs deal with it
                demo_log_dir_path = None

            # Run demo_logs function with args
            # Reminder, if demo logs is passed demo_temp_dir=None then it will use a
            # demo_temp as set by return_demo_temp() in reader.py
            demo_logs(demo_temp_dir=demo_log_dir_path)
            # Log that the cli tool is running, with args
            logger.debug(f"Running cli-demo-logs tool with: {parsed_args}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            "Please ensure the parent directory exists and try again.", file=sys.stderr
        )
        print("e.g. a path to the repo, or within home: ~/demos", file=sys.stderr)
        sys.exit(1)

    # Note cli tools may be expected to return none or 0 for testing
    # Note when developing cli tools, check for returncode if used and
    # compare use when called via function (no code) vs CLI tool (rtn code).

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            /demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A (see pyproject.toml)
    # ===================================================================


# Note - no argparse here - uses sys.argv instead
def demo_logs_main():
    """Command to call the demo logs function, with option to set target directory.

    Creates two example demo log files within a directory.
    """
    demo_temp_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    demo_logs(demo_temp_dir=demo_temp_dir)
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            test_cli.py
    # b_integration     test_cli.py
    # c_end_to_end      test_cli.py
    # d_user_interface  test_cli.py
    # ===================================================================
