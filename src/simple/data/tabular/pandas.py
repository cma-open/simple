"""Pandas dataframes."""

# TODO move to repo - cmadata ?

from pathlib import Path

from simple.data.common import make_reference_dataframe


def make_reference_file(out_path):
    """Create reference file on disk."""
    # Set output full pth and filename
    filename = Path(out_path) / "csv_data.csv"
    # Write CSV file to disk
    df = make_reference_dataframe()
    df.to_csv(filename, index=False)
