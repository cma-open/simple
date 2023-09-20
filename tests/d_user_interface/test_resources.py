"""Tests for the resources namespace subpackage."""

from importlib.resources import files

from simple.definitions import RESOURCES

DEBUG = True


def test_data_resources():
    """Test that package resources can be accessed via namespace."""
    package_resources = files(RESOURCES)
    assert package_resources.is_dir()
    # List files expected to be within the resources directory
    expected_filenames = ["data1.txt", "data2.csv", "test_config.ini"]
    for file in package_resources.iterdir():
        if DEBUG:
            print(file)
        assert file.name in expected_filenames
        assert file.is_file()


def test_data_resources_file_content():
    """Test that data file content can be read."""
    data_text = files(RESOURCES).joinpath("data1.txt").read_text().strip()
    # See #19 re bug in editable vs user install, fixed by .strip()
    if DEBUG:
        print(data_text)
    assert data_text == "hello world"


# TODO these seem duplicates of the b_integration/test_resources.py
# TODO check and delete