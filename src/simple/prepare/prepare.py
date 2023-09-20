"""Prepare module provides data conversion and preparation code."""


def add_small_constant(input_value: int | float) -> float:
    """Add small constant decimal value to the input value.

    Parameters
    ----------
    input_value : int | float
        Input value to which the constant will be added

    Returns
    -------
    float
        Returns value calculated from input_value plus constant

    """
    result = input_value + 0.000005
    return result

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            test_prepare.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================


def convert_to_string(input_value: int | float) -> str:
    """Convert input values to string.

    Parameters
    ----------
    input_value : int | float
        Input value, to be converted

    Returns
    -------
    str
        String representation of the input
    """
    string = str(input_value)
    return string

    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            test_prepare.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================
