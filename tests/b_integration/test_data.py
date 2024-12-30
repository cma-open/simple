"""Tests for the netcdf data module."""


from importlib.metadata import version
from unittest.mock import patch

import netCDF4 as nc

from simple.definitions import PACKAGE
from simple.netcdf.data import add_metadata, create_d, main

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible

# Take the version number from the package version in setup
PKG_VERSION = version(PACKAGE)


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


def test_main_integration(tmp_path):
    """Test for main function."""
    # This function mainly calls other functions
    # Integration test checks these are called and all implemented together correctly
    with patch("simple.netcdf.data.DATAFILE", "data_test.nc"):
        with patch("simple.netcdf.data.return_outputs", return_value=tmp_path):
            main(cf_version="CF:TEST")
            # Test file created
            simple_netcdf_file = tmp_path / "data_test.nc"
            assert simple_netcdf_file.is_file()
            with nc.Dataset(simple_netcdf_file, mode="r") as ds:
                # Test metadata added
                assert ds.title == "test title"
                assert ds.description == "Example dataset containing one group"
                assert "Created " in ds.history
                assert (
                    ds.source == f"SIMPLE python package. Version: simple-{PKG_VERSION}"
                )
                # Test CF convention set
                assert ds.Conventions == "CF:TEST"
