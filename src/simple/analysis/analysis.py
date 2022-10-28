"""Analysis module to provide command line interface calculations."""

from simple.prepare.prepare import add_small_constant, convert_to_string


def duplicate(input):
    """Duplicate input values into a list."""
    result_list = [input, input]
    return result_list


def calculate(x, y):
    """Sum x and y and return result."""
    result = x + y
    result_modified = add_small_constant(result)
    result_string = convert_to_string(result_modified)
    result_list = duplicate(result_string)
    return result_list
