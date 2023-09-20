"""Unit tests for the analysis module."""

from unittest.mock import patch

from simple.analysis.analysis import calculate, duplicate


def test_duplicate():
    """Test values are duplicated into list output."""
    test_input = "test"
    output = duplicate(test_input)
    expected = ["test", "test"]
    assert output == expected


# Use mock to unit test the calculate function, also see associated integration test
# Patch out functions at the location used, not where defined
@patch("simple.analysis.analysis.duplicate")  # Note the source!
@patch("simple.analysis.analysis.convert_to_string")  # Note the source!
@patch("simple.analysis.analysis.add_small_constant")  # Note the source!
def test_calculate(mock_add_constant, mock_convert_to_string, mock_duplicate):
    """Test calculate function, mock out intermediate functions."""
    # Set the return values for the mocked functions
    mock_add_constant.return_value = 2.000005
    mock_convert_to_string.return_value = "2.000005"
    mock_duplicate.return_value = ["2.000005", "2.000005"]
    # Run calculate function (with intermediate functions mocked)
    output = calculate(1, 1)
    expected = ["2.000005", "2.000005"]
    # Check output is as expected
    assert output == expected
