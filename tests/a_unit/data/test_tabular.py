"""Pandas dataframes."""

# TODO move to repo - cmadata ?

from simple.data.tabular.pandas import make_reference_file


def test_make_reference_file(tmp_path):
    """Test make reference file on disk."""
    make_reference_file(tmp_path)
    expected_file = "csv_data.csv"
    assert (tmp_path / expected_file).is_file()


# TODO - fix later

# def test_csv_loader_get():
#     """Test load of CSV files into DF."""
#     # Path for test data file on disk.
#     test_dir = Path(__file__).parent
#     csv_file = test_dir / "test_data" / "csv_data.data"
#
#     # Create DataFrame object and load the contents of a data file into it.
#     g_df = pd.read_csv(filepath_or_buffer=csv_file)
#
#     # Assert that returned obs_structure is of type Structure.
#     assert isinstance(g_df, pd.DataFrame)
#
#     print(g_df)

# Assert that obs_structure.data matches the reference dataframe.
# pd.testing.assert_frame_equal(obs_structure.data, reference_dataframe)


# def test_csv_loader_write(reference_dataframe, tmp_path):
#     """Test load of CSV files into Structure with CSVLoader"""

#     # Path for test data file on disk.
#     csv_file = tmp_path / 'test_data.data'

#     # Create a Structure to have contents writen to disk
#     test_df = make_reference_dataframe()

#     # Create CSVLoader object to load the contents of a data file into a Structure.
#     csv_loader = CSVLoader.write_structure(test_structure, csv_file)

#     # Load Structure from the file.
#     loaded_structure = CSVLoader(csv_file).get_structure()

#     # Assert that loaded_structure.data matches the reference dataframe.
#     pd.testing.assert_frame_equal(loaded_structure.data, reference_dataframe)


# def test_csv_writer(make_reference_dataframe, tmp_path):
#     """Test write of DF to CSV."""
#     # TODO move to tests dir
#
#     # Path for test data file on disk.
#     csv_file = tmp_path / "test_data_out.data"
#
#     # Create a Structure to have contents writen to disk
#     test_df = make_reference_dataframe
#
#     test_df.to_csv(path_or_buf=csv_file)

# Assert that file created
