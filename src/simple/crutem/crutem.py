"""Crutem data and nctoolkit examples."""

# link to nctoolkit notes here

# TODO se issue #27

import nctoolkit as nc

# access crutem anomaly file


def open_crutem_file(infile):
    """Open crutem netcdf data from local file."""
    ds = nc.open_data(infile)
    return ds


def get_crutem_from_url():
    """Open crutem netcdf data file from URL."""
    url = (
        "https://www.metoffice.gov.uk/hadobs/crutem5/data/"
        "CRUTEM.5.0.1.0/grids/CRUTEM.5.0.1.0.anomalies.nc"
    )
    with nc.open_url(url) as ds:
        return ds


def crop_to_europe(ds):
    """Geospatial crop netcdf data file."""
    ds.crop(lon=[-13, 38], lat=[30, 67])
    return ds


def subset_10_years(ds):
    """.Extract years from netcdf data file."""
    ds.subset(years=[2000, 2001, 2002, 2003, 2004, 2005])
    return ds


# ds.check()
