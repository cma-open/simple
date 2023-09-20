"""Integration tests for system resources (files)."""

from importlib.resources import files

from simple.definitions import RESOURCES

DEBUG = False


def test_resources_files():
    """Test that the system resources dir holds expected files."""
    package_resources = files(RESOURCES)
    assert package_resources.is_dir()
    # List files expected to be within the resources directory
    expected_filenames = ["data1.txt", "data2.csv", "test_config.ini"]
    for file in package_resources.iterdir():
        if DEBUG:
            print(file)
        assert file.name in expected_filenames
        assert file.is_file()
