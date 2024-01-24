"""File and data input / output."""

import logging
from pathlib import Path

from simple.common.common import clean_directory
from simple.config.reader import return_datadir, return_outputs, return_verbosity

# Get current datadir and outputs from config
DATADIR = return_datadir()
OUTPUTS = Path(DATADIR) / return_outputs()

# List of data files generated and used within the system.
FILES = ["test.nc", "other.nc", "data.nc", "more.txt"]

logger = logging.getLogger(__name__)


def main():
    """Remove a known set of files from the outputs directory."""
    if return_verbosity():
        logger.debug(f"Removing any existing data files {FILES} from: {OUTPUTS}")
    clean_directory(dir_path=OUTPUTS, files=FILES)
    logger.info(f"Data removed from: {OUTPUTS}")


# ==================================================================================
# Test type and location (training use)
# ----------------------------------------------------------------------------------
# a_unit  test_io.py
# b_integration  test_io.py
# c_end_to_end  n/a
# d_user_interface  n/a
# ==================================================================================
