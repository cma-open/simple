"""Tests for the io module."""

# Test individual functions in isolation to ensure they work as expected.

from unittest.mock import patch

from simple.io.io import FILES, OUTPUTS, main

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible


# Test ensures the main function correctly calls the logger
# and clean_directory functions.
# Note the optional verbosioty level is also tested so the logger output and
# all lines of code can be tested
@patch("simple.io.io.return_verbosity", return_value=True)
@patch("simple.io.io.clean_directory")
@patch("simple.io.io.logger")
def test_main_function(mock_logger, mock_clean_directory, mock_return_verbosity):
    """Test for main function."""
    main()
    # Check if the debug log is called with the correct message
    mock_logger.debug.assert_called_with(
        f"Removing any existing data files {FILES} from: {OUTPUTS}"
    )
    # Check if the clean_directory function is called with the correct arguments
    mock_clean_directory.assert_called_with(dir_path=OUTPUTS, files=FILES)
    # Check if the info log is called with the correct message
    mock_logger.info.assert_called_with(f"Data removed from: {OUTPUTS}")
