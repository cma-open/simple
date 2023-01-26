"""Tests for the common subpackage."""

import pytest

from simple.common.common import clean_directory

# List of data files generated and used within the system.
FILES = ["test.nc", "other.nc", "more.txt"]


@pytest.fixture
def create_files(tmp_path):
    """Create test files."""
    # Fixture to create named files from list int tmp_path
    for file in FILES:
        filepath = tmp_path / file
        filepath.touch()


def test_clean_directory(tmp_path, create_files):
    """Test clean_directory function."""
    print("Files exist:")
    [print(file) for file in tmp_path.iterdir()]
    # clean directory
    clean_directory(tmp_path, FILES)
    contains_files = any(tmp_path.iterdir())  # False if empty
    assert contains_files is False
    print("Files in tmp_path:")
    [print(file) for file in tmp_path.iterdir()]
