"""Tests for the netcdf data module."""


import netCDF4 as nc

from simple.netcdf.data import add_metadata, create_d

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible


def test_add_metadata(tmp_path):
    """Test for add_metadata function."""
    test_filename = "test.nc"
    test_file = tmp_path / test_filename
    create_d(netcdf=test_file)
    add_metadata(test_file)
    # Check file has metadata present (only a selectino tested)
    with nc.Dataset(test_file, mode="r") as ds:
        assert ds.title == "test title"
        assert ds.description == "Example dataset containing one group"
