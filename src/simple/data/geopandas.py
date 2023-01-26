"""Geopandas dataframes."""

from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point

from simple.data.common import make_reference_dataframe


def make_reference_file():
    """Create reference file on disk."""
    # Set output location
    test_dir = Path(__file__).parent
    filename = test_dir / "test_data" / "llllll_data.data"

    # Write CSV file to disk
    df = make_reference_dataframe()
    df.to_csv(filename, index=False)


def test_spatial_dataframe(make_reference_dataframe):
    """Test spatial dataframe."""
    # TODO move to tests dir
    # Create a Structure to have contents writen to disk
    test_df = make_reference_dataframe

    crs = {"init": "epsg:4326"}
    geometry = [Point(xy) for xy in zip(test_df["longitude"], test_df["latitude"])]

    geodata = gpd.GeoDataFrame(test_df, crs=crs, geometry=geometry)

    print(geodata)

    # geodata.plot()
