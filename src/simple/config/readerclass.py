"""Read values from user editable configuration file."""

import configparser

from simple.definitions import PACKAGE_DIR

config = configparser.ConfigParser()

# Set path to user edited config file
configfile = f"{PACKAGE_DIR}/config.ini"
# Not supplied with docstring so filepath is not visible in sphinx docs


class SourceData:
    """Class to read config values from ini file based on selected user options.

    A simple interface to get values from the user editable configuration file, based
    on selections made by the user.Used by the command line interface (CLI) tool
    for data download.

    Parameters
    ----------
    service : str
        Service name of the data download server. Possible selections are set within
        :func:`cmatools.cli_data_download.cli_parser`.
    dataset : str
        Dataset name to be downloaded. Possible selections are set within
        :func:`cmatools.cli_data_download.cli_parser`.

    Attributes
    ----------
    service : str
        Data download service name
    dataset : str
        Dataset name to be downloaded
    """

    def __init__(self):
        self.inputs = None
        self.outputs = None
        self.archives = None
        # self.long = None
        # self.format = None
        # self.server = None
        # self.filename = None

    def read_input_source_ini(self):
        """Read input sources from the ini config file."""
        config.read(configfile)

        self.inputs = config.get("DATADIR", "INPUTS")
        self.outputs = config.get("DATADIR", "OUTPUTS")
        self.archives = config.get("DATADIR", "ARCHIVES")

    # pylint: disable=R0201
    def validate(self):
        """Validate the ini config file values."""
        # Not used
        # TODO - add example code, remove pylist disable when done
        return False
