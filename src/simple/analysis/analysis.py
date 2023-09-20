"""Analysis module to provide command line interface calculations."""

from simple.prepare.prepare import add_small_constant, convert_to_string

# Note / Reminder
# These are just example functions to illustrate testing, as either single functions
# or functions that also contain other functions.


def duplicate(input_value: str) -> list:
    """Duplicate input values into a list.

    Parameters
    ----------
    input_value : str
        String input value

    Returns
    -------
    list
        A 2 item list with the input str value duplicated
    """
    input_list = [input_value, input_value]
    return input_list

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            analysis/test_analysis.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def calculate(x: int, y: int) -> list:
    """Sum x and y, apply modifications, and return result.

    Parameters
    ----------
    x : int
        Input x

    y : int
        Input y

    Returns
    -------
    list
        Calculation result
    """
    # Add the two integers
    result = x + y
    # Apply modification function
    result_modified = add_small_constant(result)
    # Convert output to a string
    result_string = convert_to_string(result_modified)
    # Duplicate the strings into a list
    result_list = duplicate(result_string)
    return result_list

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            analysis/test_analysis.py
    # b_integration     test_analysis_analysis.py
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================
