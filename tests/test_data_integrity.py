"""Data-integrity tests for the NYC Airbnb 2019 dataset.

These guard the analysis against a corrupted, truncated, or wrong-schema
dataset, so the notebook's results stay reproducible. They run with just
pandas + pytest (no notebook execution needed), keeping CI fast and green.
"""

import os

import pandas as pd
import pytest

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "AB_NYC_2019.csv")

EXPECTED_COLUMNS = [
    "id", "name", "host_id", "host_name", "neighbourhood_group",
    "neighbourhood", "latitude", "longitude", "room_type", "price",
    "minimum_nights", "number_of_reviews", "last_review",
    "reviews_per_month", "calculated_host_listings_count", "availability_365",
]

NYC_BOROUGHS = {"Brooklyn", "Manhattan", "Queens", "Staten Island", "Bronx"}


@pytest.fixture(scope="module")
def df():
    assert os.path.exists(DATA_PATH), "dataset missing — the repo should ship data/AB_NYC_2019.csv"
    return pd.read_csv(DATA_PATH)


def test_row_count(df):
    # the published Kaggle 2019 dataset has exactly 48,895 listings
    assert len(df) == 48895


def test_schema(df):
    assert list(df.columns) == EXPECTED_COLUMNS


def test_price_is_non_negative(df):
    assert df["price"].min() >= 0


def test_boroughs_are_the_five_nyc_ones(df):
    assert set(df["neighbourhood_group"].unique()) == NYC_BOROUGHS


def test_key_columns_have_no_nulls(df):
    for col in ("id", "price", "room_type", "neighbourhood_group"):
        assert df[col].notna().all(), f"{col} should have no missing values"


def test_room_types_present(df):
    assert {"Entire home/apt", "Private room", "Shared room"}.issubset(set(df["room_type"].unique()))
