"""Tests for the netcdf module."""

from datetime import datetime
from importlib.metadata import version

import netCDF4 as nc
import numpy as np
import pytest

from simple.definitions import PACKAGE
from simple.netcdf.data import add_metadata, create_d, set_cf_convention_level
from simple.netcdf.tools import (
    print_netcdf_content,
    print_netcdf_dimensions,
    print_netcdf_variables,
)

# Take the version number from the package version in setup
PKG_VERSION = version(PACKAGE)


# Create pytest fixtures for use in testing


@pytest.fixture
def create_base(tmp_path):
    """Create a basic netcdf data file."""
    # Set filename, mode and type
    netcdf = tmp_path / "base.nc"
    with nc.Dataset(netcdf, mode="w", format="NETCDF4") as ds:
        # Create dimensions
        ds.createDimension("time", None)
        ds.createDimension("lat", 10)
        ds.createDimension("lon", 10)
    return netcdf


@pytest.fixture
def create_test_data(tmp_path):
    """Create a netcdf data file with variables."""
    # Set filename, mode and type
    netcdf = tmp_path / "test.nc"
    with nc.Dataset(netcdf, mode="w", format="NETCDF4") as ds:
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
        value[0, :, :] = np.random.uniform(
            0, 100, size=(10, 10)
        )  # uniform random values
        # TODO add detailed comments
        xval = np.linspace(0.5, 5.0, 10)
        yval = np.linspace(0.5, 5.0, 10)
        value[1, :, :] = np.array(xval.reshape(-1, 1) + yval)  # linear gradient values
        # Add global attributes
        ds.title = "test title"
        ds.description = "Example dataset containing one group"
        today = datetime.today()
        ds.history = "Created " + today.strftime("%d/%m/%y")
        ds.source = f"Python package. Version: {PACKAGE}-{PKG_VERSION}"
    return netcdf


# --- Tests for the tools module ---


def test_print_netcdf_content(create_test_data, capsys):
    """Test the netcdf print output to stdout."""
    # call function with test data
    print_netcdf_content(create_test_data)
    # access stdout/stderr output created during test execution.
    captured = capsys.readouterr()
    expected = "Dataset metadata\n"
    assert expected in captured.out
    # note - just a simple example to access and test stdout from functions
    # note - usinf capsys suppresses the normal output in test report (see test below)


def test_print_netcdf_content_view(create_test_data):
    """Test the netcdf print output to stdout."""
    # call function with test data
    print_netcdf_content(create_test_data)
    # note - this simple test is used to view output in the test report view


def test_print_netcdf_variables(create_test_data, capsys):
    """Test the netcdf print variables output to stdout."""
    # call function with test data
    print_netcdf_variables(create_test_data)
    # access stdout/stderr output created during test execution.
    captured = capsys.readouterr()
    expected = "Variables\n"
    assert expected in captured.out
    # note - just a simple example to access and test stdout from functions
    # note - this suppresses the normal output in test report (see test below)


def test_print_netcdf_variables_view(create_test_data):
    """Test the netcdf print variables output to stdout."""
    # call function with test data
    print_netcdf_variables(create_test_data)
    # note - simple test can be used to view print output in test report view


def test_print_netcdf_dimensions(create_test_data, capsys):
    """Test the netcdf print dimensions output to stdout."""
    # call function with test data
    print_netcdf_dimensions(create_test_data)
    # access stdout/stderr output created during test execution.
    captured = capsys.readouterr()
    expected = "Dimensions\n"
    assert expected in captured.out
    # note - just a simple example to access and test stdout from functions
    # note - this suppresses the normal output in test report (see test below)


def test_print_netcdf_dimensions_view(create_test_data):
    """Test the netcdf print dimensions output to stdout."""
    # call function with test data
    print_netcdf_dimensions(create_test_data)
    # note - simple test can be used to view print output in test report view


# --- Tests for the data module ---


def test_create_d(tmp_path):
    """Test data creation."""
    netcdf = tmp_path / "test.nc"
    create_d(netcdf)
    # test file has been created
    assert netcdf.is_file()
    # test file is a valid netcdf
    with nc.Dataset(netcdf, mode="r", format="NETCDF4") as ds:
        assert isinstance(ds, nc.Dataset)


def test_add_metadata(create_base):
    """Test add metadata to the netcdf file."""
    add_metadata(create_base)
    today = datetime.today()
    with nc.Dataset(create_base, mode="r", format="NETCDF4") as ds:
        # check the range of metadata added to the file
        expected_title = "test title"
        expected_description = "Example dataset containing one group"
        expected_history = "Created " + today.strftime("%d/%m/%y")
        assert ds.title == expected_title
        assert ds.description == expected_description
        assert ds.history == expected_history


def test_add_cf(create_base):
    """Test add cf convention level."""
    set_cf_convention_level(create_base, cf="test-value")
    with nc.Dataset(create_base, mode="r", format="NETCDF4") as ds:
        # check the cf convention
        expected_cf = "test-value"
        assert ds.Conventions == expected_cf
