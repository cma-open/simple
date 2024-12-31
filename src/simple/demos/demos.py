"""Code for all system demos.

Example:
-------
    demo_logs
    Two logs are created within a temp demo directory
    Allows easy viewing of log file format and content

    Called via command line as set in pyproject.toml

    $ demo-logs

"""
import argparse
import logging
import sys
from pathlib import Path

from simple.config.reader import return_demo_temp
from simple.logger.log import (
    console_formatter,
    create_config_logger,
    create_system_logger,
)

system_logger = logging.getLogger(__name__)

# Set demo test constants
DEMO_TEMP_DIR = return_demo_temp()
# Set logger names
DEMO_CONFIG_LOGGER_NAME = "DemoConfigLog"
DEMO_SYSTEM_LOGGER_NAME = "DemoSystemLog"
# Set demo log filenames
DEMO_CONFIG_LOG_FILE = "demo_config.log"
DEMO_SYSTEM_LOG_FILE = "demo_system.log"

# Dev notes- content
# demo_config_file_log
# demo_system_console_log
# demo_logs
# demo_logs_cli_entry_point


def demo_config_file_log(log_path):
    """Demo of log file write and content."""
    # No console handler so no terminal output
    logger = create_config_logger(
        log_path=log_path, logger_name=DEMO_CONFIG_LOGGER_NAME
    )
    # Log message to write to the config log file
    logger.debug("Config demo_temp started")
    logger.info("Config demo_temp")
    logger.debug("Config demo_temp finished")

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def demo_system_console_log(log_path: Path, logger_name: str = None):
    """Demo of system console log write and content.

    Parameters
    ----------
    log_path : Path
       Full path to output log file

    Returns
    -------
    logger : logging.Logger
    """
    # Reminder - info level and above goes to console
    # debug level and above go to file
    # Reminder create_system_logger gets logger by name, but defaults to package logger
    # Then sets level and adds file handler only, it assumes that the console handler
    # exists already
    # Therefore for the DEMO - create a new logger instead of PACKAGE level logger
    # and add a system console handler
    if logger_name is None:
        logger_name = DEMO_SYSTEM_LOGGER_NAME
    # Set logger name - create new logger
    logger = logging.getLogger(logger_name)
    # Set initial logging level (required)
    logger.setLevel(level=logging.DEBUG)
    # Add console handler
    # Set default handler name if no argument supplied
    handler_name = "DemoSystemConsoleHandler"
    # Create console log stream handler
    console_handler = logging.StreamHandler()
    # Name the console handler via argument or default
    console_handler.name = handler_name
    # Set level for console outputs - only info level and above
    console_handler.setLevel(logging.INFO)
    # Set the output format for the logger content
    console_handler.setFormatter(console_formatter)
    # Add handler to the logger
    logger.addHandler(console_handler)
    file_handler_name = "DemoSystemFileHandler"
    # Update the demo logger with file logger
    create_system_logger(
        log_path=log_path,
        logger_name=logger_name,
        file_handler_name=file_handler_name,
    )
    # All log messages go to log file
    # Additionally info level and above go to console
    logger.debug("System demo_temp started")  # File only
    logger.info("System demo_temp")  # File and console
    logger.debug("System demo_temp finished")  # File only
    return logger

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def demo_logs(demo_temp_dir=None):
    """Demo for log setup and creation."""
    # Dev Note - all log files should be ignored via vcs
    # Note - for dev install demo_temp will be within repo
    # Note - for a full installation demo_temp will be within datadir root
    if demo_temp_dir is None:
        demo_temp_dir = DEMO_TEMP_DIR
    # Create DEMO_TEMP_DIR if not yet existing
    demo_temp_dir.mkdir(exist_ok=True)
    # Set full path location for demo_temp log files x2
    demo_system_log = demo_temp_dir / "demo_system.log"
    demo_config_log = demo_temp_dir / "demo_config.log"
    # Run the demo to create console logs - including demo log messages
    demo_system_console_log(log_path=demo_system_log)
    # Run the demo to create config file logs - including demo log messages
    demo_config_file_log(log_path=demo_config_log)
    # Add an extra log message at system level
    # NOTE - reminder this is to main system logger, not demo logger
    system_logger.info(f"Demo logs has run - see files in {demo_temp_dir}")

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            demos/test_demo_logs.py
    # b_integration     test_demo_logs.py
    # c_end_to_end      N/A
    # d_user_interface  N/A (see pyproject.toml)
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

    # START - go through all dmeo tets ..
    # Added to facilitate testing with no args
    # if argv is None:
    #    argv = []

    parser = argparse.ArgumentParser(
        prog="CLI-DEMO-LOGS",
        description="A command line tool to demo logs.",
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
            system_logger.debug(f"{parser.prog} command run in dry-run mode. Exiting")

        else:
            # For any set demo_temp paths, ensure Path object
            if parsed_args.demo_log_dir:
                # Convert back to a path object
                demo_log_dir_path = Path(parsed_args.demo_log_dir)
                parent_directory = demo_log_dir_path.parent
                if parent_directory.exists() and parent_directory.is_dir():
                    system_logger.debug(
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
            system_logger.debug(f"Running cli-demo-logs tool with: {parsed_args}")

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
    # a_unit            TODO
    # b_integration     TODO
    # c_end_to_end      ?
    # d_user_interface  N/A (see pyproject.toml)
    # ===================================================================
