"""
Module to read in settings from config file.

TODO raise issue
leaving in repo for now - convert to an alternative example reader
"""

import datetime
import os

import yaml
from jinja2 import DebugUndefined, Environment, FileSystemLoader

from simple.definitions import PACKAGE_DIR

CONFIG = "config.ini"

DATADIR = "x"  # take from config

# Runtime variables to be writen into the configuration at runtime
runtime_vars = {
    "build_time": datetime.datetime.now().isoformat(timespec="seconds"),
    "data_dir": DATADIR,
}


class SystemConfig:
    """Store the contents of the system config file and manage configuration I/O.

    Parameters
    ----------
        config_path:
            Path to directory containing configuration files.
        config_file:
    """

    def __init__(self, config_path=PACKAGE_DIR, config_file=CONFIG):
        self.config_path = config_path
        self.config_file = config_file
        self.data = None
        self.read_config()

    def read_config(self):
        """Load configuration containing values to be inserted into the template."""
        # fullpath = Path(PACKAGE_DIR) / CONFIG
        # print(fullpath)
        # with open(fullpath) as config_content:
        # Load the global configuration
        # config_content = yaml.safe_load(fullpath)
        # pass
        # Load the main template configuration.
        # Uses DebugUndefined to leave undefined jinja2 variables in place.
        templateEnv = Environment(
            loader=FileSystemLoader(searchpath=self.config_path),
            autoescape=True,
            undefined=DebugUndefined,
        )
        template_configuration = templateEnv.get_template(self.config_file)
        # Render the template and load into dictionary
        self.rendered_config = template_configuration.render(**globals, **runtime_vars)
        self.data = yaml.safe_load(self.rendered_config)

    def write_config(self, config_file):
        """Write the rendered configuration document to disk.

        Write the contents of self.rendered_config to disk,
        complete with full formatting and comments.
        """
        with open(config_file, "w") as f:
            f.write(self.rendered_config)

    def write_config_data(self, config_file):
        """Write the contents of the loaded configuration data to disk.

        Writes the contents of self.data to a yaml file.
        Formatting and comments will not be preserved in the output.
        """
        with open(config_file, "w") as f:
            yaml.dump(self.data, f)

    @staticmethod
    def _build_path(directory):
        """Create a directory tree down to the indicated directory."""
        try:
            os.makedirs(directory, exist_ok=True)
        except RuntimeError:
            raise RuntimeError('Failed to create directory: "{}"'.format(directory))

    @staticmethod
    def _validate_path(directory):
        """Ensure that the path to a directory exists."""
        if not os.path.isdir(directory):
            raise RuntimeError('Directory does not exist: "{}"'.format(directory))

    @staticmethod
    def _check_access(directory):
        """Ensure that write access is available for the indicated directory."""
        if not os.access(directory, os.W_OK):
            raise RuntimeError('Unable to write to directory "{}"'.format(directory))


if __name__ == "__main__":
    system_config = SystemConfig()
    print(system_config.rendered_config)
    print(system_config.data)
