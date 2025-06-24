"""Tests for the data example module."""

from simple.data.example.example import create_example_data_file


def test_create_data_file(tmp_path) -> None:
    """
    Test for the create_example_data_file function.

    Ensure function creates a file with the correct data.

    Parameters
    ----------
    tmp_path : pathlib.Path
        A temporary directory provided by pytest.

    Asserts
    -------
    The file is created.
    The file contains the correct data.
    """
    # Define the filename and data for testing
    test_filename = tmp_path / "test_data_file.txt"
    test_data = "This is a test data file."

    # Call the function to create the file
    create_example_data_file(test_filename, test_data)

    # Check if the file was created
    assert test_filename.is_file(), "File was not created."

    # Check if the file contains the correct data
    with open(test_filename, "r") as file:
        content = file.read()
    assert content == test_data, "File content does not match."
