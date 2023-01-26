"""Selected functions to view netcdf content."""

# some examples from https://pyhogs.github.io/intro_netcdf4.html
# some examples from https://opensourceoptions.com/blog/create-netcdf-files-with-python/

import netCDF4 as nc


def print_netcdf_content(netcdf):
    """Print netcdf file metadata."""
    with nc.Dataset(netcdf, "r") as ds:
        print("-------------------")
        print("Dataset metadata")
        print(ds)
        print("-------------------")


def print_netcdf_variables(netcdf):
    """Print netcdf variables."""
    print()
    print("Variables")
    print("----------")
    with nc.Dataset(netcdf, "r") as ds:
        for var in ds.variables.values():
            print(var)
            print()


def print_netcdf_dimensions(netcdf):
    """Print netcdf dimensions.."""
    print()
    print("Dimensions")
    print("----------")
    with nc.Dataset(netcdf, "r") as ds:
        for dim in ds.dimensions.values():
            print(dim)
