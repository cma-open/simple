"""Prepare module provides data conversion and preparation code."""


def add_small_constant(input_value):
    """Add small constant decimal value to the input value."""
    result = input_value + 0.000005
    return result


def convert_to_string(input_value):
    """Convert input values to string."""
    string = str(input_value)
    return string
