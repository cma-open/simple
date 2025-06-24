"""Tests for the netcdf module."""

# Test individual functions in isolation to ensure they work as expected.


from importlib.metadata import version
from unittest.mock import patch

import netCDF4 as nc
import numpy as np
import pytest

from simple.definitions import PACKAGE
from simple.netcdf.data import (
    add_metadata,
    create_d,
    main,
    return_outfile,
    set_cf_convention_level,
)

# Take the version number from the package version in setup
PKG_VERSION = version(PACKAGE)

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible


@pytest.fixture
def simple_netcdf_file(tmp_path):
    """Pytest netcdf test fixture."""
    # Define the path for the NetCDF file
    file_path = tmp_path / "test_file.nc"

    # Create a new NetCDF file
    with nc.Dataset(file_path, "w", format="NETCDF4") as ds:
        # Create dimensions
        ds.createDimension("x", 10)
        ds.createDimension("y", 10)

        # Create variables
        var = ds.createVariable("data", np.float32, ("x", "y"))

        # Assign data to the variable
        var[:] = np.random.rand(10, 10)

        # Return the path to the NetCDF file
        return file_path


def test_return_outfile(tmp_path):
    """Test for return_outfile function."""
    test_filename = "test.nc"
    result = return_outfile(tmp_path, test_filename)
    expected = tmp_path / test_filename
    assert result == expected, f"Expected {expected}, but got {result}"


def test_create_d(tmp_path):
    """Test for create_d function."""
    test_filename = "test.nc"
    test_file = tmp_path / test_filename
    create_d(netcdf=test_file)
    assert test_file.is_file()
    # Verify that the file is a valid NetCDF file
    try:
        with nc.Dataset(test_file, "r") as ds:
            # Check if the file has any dimensions or variables (basic validity check)
            assert (
                len(ds.dimensions) > 0 or len(ds.variables) > 0
            ), "NetCDF file should have dimensions or variables"
    except Exception as e:
        pytest.fail(f"Failed to open or validate NetCDF file: {e}")


def test_add_metadata(tmp_path, simple_netcdf_file):
    """Test for add_metadata function."""
    # Add metadata
    add_metadata(simple_netcdf_file)
    # Test
    with nc.Dataset(simple_netcdf_file, mode="r") as ds:
        assert ds.title == "test title"
        assert ds.description == "Example dataset containing one group"
        assert "Created " in ds.history
        assert ds.source == f"SIMPLE python package. Version: simple-{PKG_VERSION}"


def test_set_cf_convention_level(simple_netcdf_file):
    """Test for set cf convention level."""
    set_cf_convention_level(simple_netcdf_file, cf_version="test_example")
    # Test
    with nc.Dataset(simple_netcdf_file, mode="r") as ds:
        assert ds.Conventions == "test_example"


def test_main(tmp_path):
    """Test for main function."""
    # This function mainly calls other functions
    # Unit test checks these are called with correct arguments, where applicable
    with patch("simple.netcdf.data.return_outfile") as mock_return_outfile, patch(
        "simple.netcdf.data.create_d"
    ) as mock_create, patch(
        "simple.netcdf.data.add_metadata"
    ) as mock_add_metadata, patch(
        "simple.netcdf.data.set_cf_convention_level"
    ) as mock_set_cf_convention:
        # Set test arguments
        file_path = tmp_path / "test_netcdf.nc"
        cf_version = "CF-111"
        # Set retun for mocked return_outfile
        mock_return_outfile.return_value = file_path
        # Call function
        main(cf_version=cf_version)
        # check all component fnctions wer called a expected
        mock_return_outfile.assert_called_once()
        mock_create.assert_called_once_with(file_path)
        mock_add_metadata.assert_called_once_with(file_path)
        mock_set_cf_convention.assert_called_once_with(file_path, cf_version=cf_version)


def test_main_debug(tmp_path):
    """Test for main function, with debug."""
    # This function mainly calls other functions
    # Unit test checks these are called with correct arguments, where applicable
    with patch("simple.netcdf.data.return_outfile") as mock_return_outfile, patch(
        "simple.netcdf.data.create_d"
    ) as mock_create, patch(
        "simple.netcdf.data.add_metadata"
    ) as mock_add_metadata, patch(
        "simple.netcdf.data.set_cf_convention_level"
    ) as mock_set_cf_convention, patch(
        "simple.netcdf.data.print_netcdf_content"
    ) as mock_print_netcdf, patch(
        "simple.netcdf.data.print_netcdf_dimensions"
    ) as mock_print_dimensions, patch(
        "simple.netcdf.data.print_netcdf_variables"
    ) as mock_print_variables:
        # Set test arguments
        file_path = tmp_path / "test_netcdf.nc"
        cf_version = "CF-111"
        # Set retun for mocked return_outfile
        mock_return_outfile.return_value = file_path
        # Call function
        main(debug=True, cf_version=cf_version)
        # check all component functions were called a expected
        mock_return_outfile.assert_called_once()
        mock_create.assert_called_once_with(file_path)
        mock_add_metadata.assert_called_once_with(file_path)
        mock_set_cf_convention.assert_called_once_with(file_path, cf_version=cf_version)
        # also expect print functions were called where debug is True
        mock_print_netcdf.assert_called_once()
        mock_print_dimensions.assert_called_once()
        mock_print_variables.assert_called_once()
