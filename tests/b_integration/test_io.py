"""Tests for the io module."""

from unittest.mock import patch

import pytest

from simple.config.reader import return_verbosity
from simple.io.io import FILES, main


@pytest.fixture
def create_files(tmp_path):
    """Create test files."""
    # Fixture to create named files from list in tmp_path
    for file in FILES:
        filepath = tmp_path / file
        filepath.touch()


def test_main(tmp_path, create_files):
    """Test main function from io module."""
    # Main function removes files from DATADIR
    with patch("simple.io.io.OUTPUTS", tmp_path):
        # Mock outputs and replace with tmp_path
        # Create files in tmp_path via fixture
        files = [file for file in tmp_path.iterdir()]
        # Print files to the test report for debugging if editable and verbose set
        if return_verbosity():
            print("Files exist in tmp_path:")
            print(*files, sep="\n")
        # Run main function to remove files
        main()
        # Check if any files exist in tmp_path
        contains_files = any(tmp_path.iterdir())  # False if empty
        # Confirm tmp_path is empty
        assert contains_files is False
        # Print files to the test report for debugging if editable and verbose set
        if return_verbosity():
            print("Files in tmp_path:")
            files = [file for file in tmp_path.iterdir()]
            print(*files, sep="\n")
            if len(files) < 1:
                print("No files in tmp_path")
