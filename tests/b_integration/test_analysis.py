"""Integration tests for the analysis module."""

from simple.analysis.analysis import calculate


def test_calculate():
    """Test calculate function."""
    output = calculate(1, 1)
    expected = ["2.000005", "2.000005"]
    assert output == expected
