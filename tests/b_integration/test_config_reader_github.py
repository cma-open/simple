"""Tests for the config subpackage."""

import importlib
from importlib.resources import files
from pathlib import PosixPath
from unittest.mock import patch

from simple.definitions import RESOURCES

GITHUB_CONFIGFILE = files(RESOURCES) / "github_config.ini"


# Note these integration tests run against static test files
# This allows full process to be tested

# First quick integratino test to check that the github focussed  config ini file
# exists and is able to be read


def test_return_datadir_full_install_github():
    """Test return_datadir function via github ini."""
    with patch.dict("os.environ", {"GITHUB_ACTIONS": "true"}):
        import simple.config.reader

        importlib.reload(simple.config.reader)
        from simple.config.reader import IN_GITHUB_ACTIONS, configfile, return_datadir

        assert IN_GITHUB_ACTIONS is True
        assert "simple/resources/github_config.ini" in str(configfile)
        assert configfile == GITHUB_CONFIGFILE
        with patch("simple.config.reader.check_install_status") as mock_install_status:
            # Set the return value for mocked function
            mock_install_status.return_value = "Install"
            # Get datadir (will always be a Path object)
            datadir = return_datadir()
            expected = PosixPath("/home/github/temp")
            assert datadir == expected
    # Editable and home ~ directory based confg options not tested here, see unit tests
