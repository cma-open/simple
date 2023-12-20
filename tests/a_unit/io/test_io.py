"""Tests for the io module."""

from unittest.mock import patch

from simple.config.reader import return_verbosity
from simple.io.io import main


@patch("simple.io.io.clean_directory")  # Note the source!
def test_main(mock_clean_directory, capsys, caplog):
    """Test main function from io module."""
    # Main function remove files from DATADIR
    # TODO review coverage and test type
    main()
    # Check that the mocked function was called
    mock_clean_directory.assert_called_once()

    # Some log or console stdout or stderr depends on system status settings
    # Example
    if return_verbosity():
        # Check output to stdout is as expected
        captured = capsys.readouterr()
        print(f"Stdout: {captured.out}")
        print(f"Stderr: {captured.err}")
        # Check log outputs
        expected = "Removing any existing data files "
        assert expected in caplog.text
