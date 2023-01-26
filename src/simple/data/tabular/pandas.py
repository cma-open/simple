"""Pandas dataframes."""

# TODO move to repo - cmadata ?

from pathlib import Path

from simple.data.common import make_reference_dataframe


def make_reference_file():
    """Create reference file on disk."""
    # Set output location
    test_dir = Path(__file__).parent
    filename = test_dir / "test_data" / "csv_data.data"

    # Write CSV file to disk
    df = make_reference_dataframe()
    df.to_csv(filename, index=False)
