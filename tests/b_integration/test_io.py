"""Tests for the io module."""

from unittest.mock import patch

import pytest

from simple.io.io import DEBUG, FILES, main


@pytest.fixture
def create_files(tmp_path):
    """Create test files."""
    # Fixture to create named files from list int tmp_path
    for file in FILES:
        filepath = tmp_path / file
        filepath.touch()


def test_main(tmp_path, create_files):
    """Test main function from io module."""
    # main function removes files from DATADIR
    with patch("simple.io.io.OUTPUTS", tmp_path):
        # mock outputs and replace with tmp_path
        # create files in tmp_path via fixture
        files = [file for file in tmp_path.iterdir()]
        # print files to the test report for debugging
        if DEBUG:
            print("Files exist:")
            print(*files, sep="\n")
        main()
        # confirm tmp_path is empty
        contains_files = any(tmp_path.iterdir())  # False if empty
        assert contains_files is False
        if DEBUG:
            print("Files in tmp_path:")
            files = [file for file in tmp_path.iterdir()]
            print(*files, sep="\n")
