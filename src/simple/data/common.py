"""Common functions for the data subpackage."""

import pandas as pd


#  @pytest.fixture
def make_reference_dataframe() -> pd.DataFrame:
    """Return a reference data frame for use in tests."""
    # data as a list of lists of numbers
    data = [
        [
            1,
            52.1,
            5.6,
            20.0,
            1.0,
        ],
        [
            2,
            52.2,
            6.6,
            21.0,
            2.0,
        ],
        [
            3,
            52.3,
            7.6,
            22.0,
            3.0,
        ],
        [
            4,
            52.4,
            8.6,
            23.0,
            4.0,
        ],
        [
            5,
            52.5,
            9.6,
            24.0,
            5.0,
        ],
    ]
    # header values
    columns = ["time", "latitude", "longitude", "temperature", "uncertainty"]
    return pd.DataFrame(data=data, columns=columns)
