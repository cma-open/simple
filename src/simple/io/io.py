"""File and data input / output."""

from pathlib import Path

from simple.common.common import clean_directory
from simple.config.reader import read_ini, return_outputs

# Get current datadir and outputs from config
DATADIR = read_ini()
OUTPUTS = Path(DATADIR) / return_outputs()

# List of data files generated and used within the system.
FILES = ["test.nc", "other.nc", "more.txt"]

DEBUG = True


def main():
    """Remove a known set of files from the outputs directory."""
    if DEBUG:
        print(f"Removing any existing data files from: {OUTPUTS}")
    clean_directory(dir_path=OUTPUTS, files=FILES)


# ==================================================================================
# Test type and location (training use)
# ----------------------------------------------------------------------------------
# a_unit  test_io.py
# b_integration  test_io.py
# c_end_to_end  n/a
# d_user_interface  n/a
# ==================================================================================
