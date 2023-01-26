"""Netcdf data creation."""

# some examples from https://pyhogs.github.io/intro_netcdf4.html
# some examples from https://opensourceoptions.com/blog/create-netcdf-files-with-python/

from datetime import datetime
from pathlib import Path

import netCDF4 as nc
import numpy as np
import pkg_resources

from simple.config.reader import read_ini, return_outputs
from simple.definitions import PACKAGE
from simple.netcdf.tools import (
    print_netcdf_content,
    print_netcdf_dimensions,
    print_netcdf_variables,
)

# Get current datadir and outputs from config
DATADIR = read_ini()
OUTPUTS = Path(DATADIR) / return_outputs()
TESTFILE = OUTPUTS / "test.nc"

# Take the version number from the package version in setup
PKG_VERSION = pkg_resources.get_distribution(PACKAGE).version


def create_d(netcdf, debug=None):
    """Create a netcdf data file in the data dir (as specified via config.ini)."""
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
    #  west (-180) to east (180)


def add_metadata(netcdf):
    """Add custom metadata to the file."""
    today = datetime.today()
    with nc.Dataset(netcdf, mode="a") as ds:  # note append mode
        # Add global attributes
        ds.title = "test title"
        ds.description = "Example dataset containing one group"
        ds.history = "Created " + today.strftime("%d/%m/%y")
        ds.source = f"SIMPLE python package. Version: simple-{PKG_VERSION}"
        # TODO - add distinction software version vs dataset version


def set_cf_convention_level(netcdf, cf=None):
    """Add cf convention setting."""
    with nc.Dataset(netcdf, mode="a") as ds:  # note append mode
        ds.Conventions = cf


def main(debug=None):
    """Process main netcdf file creation workflow."""
    if debug:
        print("Creating data - netcdf ")
        print(f"File: {TESTFILE}")
    create_d(TESTFILE, debug=debug)
    add_metadata(TESTFILE)
    set_cf_convention_level(TESTFILE, cf="CF:1.6")
    if debug:
        print_netcdf_content(TESTFILE)
        print_netcdf_dimensions(TESTFILE)
        print_netcdf_variables(TESTFILE)


# lat, lon = f.variables['Latitude'], f.variables['Longitude']
