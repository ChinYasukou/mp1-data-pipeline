import pandas as pd
import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    required_columns = ["record_id", "name", "rating", "category", "status"]

    result = validate_dataframe(sample_df, required_columns, ["rating"])

    assert result.shape == (98, 5)
    assert result.columns.tolist() == required_columns
    assert pd.api.types.is_numeric_dtype(result["rating"])


def test_validate_dataframe_with_missing_column(sample_df):
    required_columns = [*sample_df.columns, "nonexistent"]

    with pytest.raises(ValueError, match="nonexistent"):
        validate_dataframe(sample_df, required_columns, ["rating"])
