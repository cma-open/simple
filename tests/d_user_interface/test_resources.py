"""Tests for the resources namespace subpackage."""

from importlib.resources import files

from simple.config.reader import return_verbosity
from simple.definitions import RESOURCES


def test_data_resources():
    """Test that package resources can be accessed via namespace."""
    package_resources = files(RESOURCES)
    assert package_resources.is_dir()
    # List files expected to be within the resources directory
    expected_filenames = [
        "data1.txt",
        "data2.csv",
        "test_config.ini",
        "github_config.ini",
    ]
    for file in package_resources.iterdir():
        # Print filename if verbose level for editable installs
        if return_verbosity():
            print(f"Expected files: {expected_filenames}")
            print(f"File present: {file}")
        assert file.name in expected_filenames
        assert file.is_file()


def test_data_resources_file_content():
    """Test that data file content can be read."""
    data_text = files(RESOURCES).joinpath("data1.txt").read_text().strip()
    # See #19 re bug in editable vs user install, fixed by .strip()
    assert data_text == "hello world"


# TODO duplicates of the b_integration/test_resources.py
# TODO check
