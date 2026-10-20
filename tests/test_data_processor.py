import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers


def test_remove_duplicates(sample_df):
    result = remove_duplicates(sample_df)

    assert len(result) == 98
    assert not result.duplicated().any()


def test_handle_missing_rows(sample_df):
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    result = handle_missing(df, axis="rows")

    assert len(result) == 97
    assert not result.isna().any().any()


def test_remove_outliers_iqr(sample_df):
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    result = remove_outliers(df, ["rating"], method="iqr", threshold=1.5)

    assert len(result) == 95


def test_remove_outliers_zscore(sample_df):
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    result = remove_outliers(df, ["rating"], method="zscore", threshold=3)

    assert len(result) == 95
    assert set(df.index) - set(result.index) == {92, 93}


def test_remove_outliers_with_unsupported_method(sample_df):
    with pytest.raises(ValueError, match="Unsupported outlier method"):
        remove_outliers(sample_df, ["rating"], method="unknown", threshold=1.5)
