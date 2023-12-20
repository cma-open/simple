"""Unit tests for the cli module."""

from datetime import datetime
from unittest.mock import patch

import netCDF4 as nc
import numpy as np
import pytest

from simple.cli import cli_data, cli_entry_point
from simple.config.reader import return_verbosity


# Patch out functions at the location used, not where defined
@patch("simple.cli.calculate")  # Note the source!
def test_cli_entry_point(mock_calculate, capsys):
    """Test cli_entry_point function ."""
    # Mock is used to set result of calculate function to focus the unit test
    # on just the entry point function
    # Calculate is called within the cli_entry_point function
    mock_calculate.return_value = ["4.000005", "4.000005"]
    # Set user inputs
    argv = ["2", "2"]
    # Run function with user inputs
    output = cli_entry_point(argv=argv)  # pylint: disable=E1111
    # Expect function to return none
    assert output is None
    # Check stdout output
    captured = capsys.readouterr()
    # Expect that function will have printed result to stdout
    expected = "['4.000005', '4.000005']\n"
    # Assert expected output in the captured.out
    assert captured.out == expected


# TODO need to add value to argv to call cli

# # Patch out functions at the location used, not where defined
# @patch("simple.netcdf.data.return_outputs")
# def test_cli_data_verbose(mock_outputs, tmp_path):
#     """Test cli_data function."""
#     # uses mock to ensure data created is temporary
#     # examines printed output from function run
#     mock_outputs.return_value = tmp_path
#     argv = ["--verbose"]
#     cli_data(argv=argv)
#     print("---")
#     print(tmp_path)
#     for item in tmp_path.iterdir():
#         print(item)

# TODO - to be a unit test, need to mock out all components ...
#  create_d(output_file, debug=debug)
#  add_metadata(output_file)
#  set_cf_convention_level(
#
# TODO - start by adding uit test at those levels ??


@pytest.fixture
def create_d(netcdf, debug=None):
    """Create a netcdf data file."""
    # Set filename, mode and type
    ds = nc.Dataset(netcdf, mode="w", format="NETCDF4")
    # Create dimensions
    ds.createDimension("time", None)
    ds.createDimension("lat", 10)
    ds.createDimension("lon", 10)
    # Create variables
    ds.createVariable("time", "f4", ("time",))
    # name variables for later modification
    lats = ds.createVariable("lat", "f4", ("lat",))
    lons = ds.createVariable("lon", "f4", ("lon",))
    value = ds.createVariable(
        "value",
        "f4",
        (
            "time",
            "lat",
            "lon",
        ),
    )
    # Set value data units
    value.units = "Unknown"
    # Add lat lon values
    lats[:] = np.arange(40.0, 50.0, 1.0)
    lons[:] = np.arange(-110.0, -100.0, 1.0)
    # Add data values
    value[0, :, :] = np.random.uniform(0, 100, size=(10, 10))  # uniform random values
    # TODO add detailed comments
    xval = np.linspace(0.5, 5.0, 10)
    yval = np.linspace(0.5, 5.0, 10)
    value[1, :, :] = np.array(xval.reshape(-1, 1) + yval)  # linear gradient values
    if debug:
        print("var size after adding first data", value.shape)
    ds.close()


def mock_add_metadata(netcdf):
    """Add custom metadata to the file."""
    today = datetime.today()
    with nc.Dataset(netcdf, mode="a") as ds:  # note append mode
        # Add global attributes
        ds.title = "test title - mocked"
        ds.description = "Example dataset containing one group - mocked"
        ds.history = "Created " + today.strftime("%d/%m/%y")


def mock_set_cf_convention_level(netcdf, cf=None):
    """Add cf convention setting."""
    with nc.Dataset(netcdf, mode="a") as ds:  # note append mode
        ds.Conventions = "cf:mocked"


@patch("simple.netcdf.data.return_outputs")
@patch("simple.netcdf.data.return_outfile")
def test_cli_data(mock_outfile, mock_outputs, tmp_path):
    """Test cli_data function."""
    # Uses mock to ensure the data created is temporary
    # Tests that data was created on disk
    # Components within cli_data include
    # return_outputs()
    # create_d()
    # add_metadata()
    # set_cf_convention_level()
    mock_outputs.return_value = tmp_path
    mock_outfile.return_value = tmp_path / "test_data.nc"
    # mock_create = ""
    # mock_cf = ""

    # run with test value (WIP)
    # verbose defaults to False

    # replace the add metadata function with the mocked version
    with patch("simple.netcdf.data.add_metadata", mock_add_metadata):
        # replace the set cf convention function with the mocked version
        with patch(
            "simple.netcdf.data.set_cf_convention_level", mock_set_cf_convention_level
        ):
            cli_data(argv=["4"])
            # Further print to stdout for verbose set editable installs
            if return_verbosity():
                print(f"Temp path: {tmp_path}")
                for item in tmp_path.iterdir():
                    print(item)
                with nc.Dataset(tmp_path / "test_data.nc") as ds:
                    print(ds)

    # cli_data(argv=["4"])
    # if DEBUG:
    #     print(f"Temp path: {tmp_path}")
    #     for item in tmp_path.iterdir():
    #         print(item)
    #     with nc.Dataset(tmp_path / "test_data.nc") as ds:
    #         print(ds)

    assert (tmp_path / "test_data.nc").is_file()


# move to user interface ? Y/N ???
def test_cli_data_version(capsys):
    """Test cli_data function."""
    # tests that funtion runs, prints version info and exists
    argv = ["--version"]
    with pytest.raises(SystemExit):
        cli_data(argv=argv)
        captured = capsys.readouterr()
        expected = "CREATE-DATA"
        assert expected in captured.out
