"""Netcdf data creation."""
import logging
from datetime import datetime
from importlib.metadata import version

import netCDF4 as nc
import numpy as np

from simple.config.reader import return_outputs
from simple.definitions import PACKAGE
from simple.netcdf.tools import (
    print_netcdf_content,
    print_netcdf_dimensions,
    print_netcdf_variables,
)

# Some examples from https://pyhogs.github.io/intro_netcdf4.html
# Some examples from https://opensourceoptions.com/blog/create-netcdf-files-with-python/


logger = logging.getLogger(__name__)

# Set output data filename
DATAFILE = "data.nc"

# Take the version number from the package version in setup
PKG_VERSION = version(PACKAGE)


def return_outfile(path, filename):
    """Return full filepath to file."""
    output_file = path / filename
    return output_file


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
    logger.debug("Creating netcdf data")
    output_file = return_outfile(return_outputs(), DATAFILE)
    if debug:
        print("Creating data - netcdf ")
        print(f"File: {output_file}")
    create_d(output_file, debug=debug)
    add_metadata(output_file)
    set_cf_convention_level(output_file, cf="CF:1.6")
    if debug:
        print_netcdf_content(output_file)
        print_netcdf_dimensions(output_file)
        print_netcdf_variables(output_file)
    logger.info(f"Netcdf data created at {output_file}")


# lat, lon = f.variables['Latitude'], f.variables['Longitude']
