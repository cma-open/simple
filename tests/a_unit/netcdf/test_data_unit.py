"""Tests for the netcdf module."""

# Test individual functions in isolation to ensure they work as expected.


import netCDF4 as nc
import pytest

from simple.netcdf.data import create_d, return_outfile

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible


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


def test_add_metadata():
    """Test for add_metadata function."""
