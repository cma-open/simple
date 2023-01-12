"""Analysis module to provide command line interface calculations."""

from simple.prepare.prepare import add_small_constant, convert_to_string


def duplicate(input_value):
    """Duplicate input values into a list."""
    input_list = [input_value, input_value]
    return input_list


def calculate(x, y):
    """Sum x and y, apply modifications, and return result."""
    result = x + y
    result_modified = add_small_constant(result)
    result_string = convert_to_string(result_modified)
    result_list = duplicate(result_string)
    return result_list
