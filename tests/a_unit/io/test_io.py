"""Tests for the io module."""

from unittest.mock import patch

from simple.io.io import DEBUG, main


@patch("simple.io.io.clean_directory")  # Note the source!
def test_main(mock_clean_directory, capsys):
    """Test main function from io module."""
    # main function remove files from DATADIR
    # TODO review coverage and test type
    main()
    # check that the mocked function was called
    mock_clean_directory.assert_called_once()
    if DEBUG:
        # check output to stdout is as expected
        captured = capsys.readouterr()
        expected = "Removing any existing data files from:"
        assert expected in captured.out
