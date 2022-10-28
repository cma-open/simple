"""Unit tests for the prepare module."""

from simple.prepare.prepare import add_small_constant, convert_to_string


def test_constant():
    """Test constant added to input values."""
    output = add_small_constant(1)
    expected = 1.000005
    assert output == expected


def test_string():
    """Test input converted to a string."""
    output = convert_to_string(10)
    expected = "10"
    assert output == expected
