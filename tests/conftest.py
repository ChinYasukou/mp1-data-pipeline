from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Read the MP1 sample CSV afresh for each test."""
    return pd.read_csv(Path("fixtures") / "sample_data.csv")
