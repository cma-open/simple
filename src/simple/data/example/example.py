"""Simple example module."""


def create_example_data_file(filename: str, data: str) -> None:
    """
    Create a data file with the given filename and write the provided data to it.

    Parameters
    ----------
    filename : str
        The name of the file to be created.
    data : str
        The data to be written to the file.

    Returns
    -------
    None
    """
    with open(filename, "w") as file:
        file.write(data)
    # ===================================================================
    # Test type and location (training use)
    # ===================================================================
    # a_unit            /data/test_example.py
    # b_integration     N/A
    # c_end_to_end      N/A
    # d_user_interface  N/A
    # ===================================================================
