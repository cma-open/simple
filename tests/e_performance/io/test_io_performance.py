"""Tests for the io module."""

import time
from unittest.mock import patch

from simple.io.io import main

# Caveat
# ======
# Code may be over-tested to ensure tests act as examples of what is possible


def test_main_performance(tmp_path):
    """
    Measure the time it takes for the main function to remove files.

    This ensures that the function performs efficiently,
    even with a large number of files.
    """
    # Setup: Create a fake output directory and a large number of files
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    files = [f"file_{i}.txt" for i in range(1000)]  # Create 1000 files
    for file in files:
        (output_dir / file).touch()

    # Patch the return values of the configuration functions
    # with patch('simple.io.io.return_datadir', return_value=str(tmp_path)), \
    #       patch('simple.io.io.return_outputs', return_value='outputs'), \
    #      patch('simple.io.io.return_verbosity', return_value=False):
    # Patch the return values of the configuration functions
    with patch("simple.io.io.OUTPUTS", output_dir), patch("simple.io.io.FILES", files):
        # Measure the start time, using perf_counter
        start_time = time.perf_counter()

        # Call the main function
        main()

        # Measure the end time
        end_time = time.perf_counter()

        # Calculate the duration
        duration = end_time - start_time

        # Verify that the function completed within an acceptable time frame
        assert (
            duration < 5
        ), f"Performance test failed: took {duration} seconds, expected <5 seconds"

    # Verify that the files have been removed
    for file in files:
        assert not (
            output_dir / file
        ).exists(), f"{file} should be removed after running main"
