import pandas as pd
from src.transform import transform_users, OUTPUT_COLUMNS

""" Test for users transformation function."""

def test_transform_users():
    users = [
        {
            "id": 1,
            "name": "  Julian Osorio ",
            "username": "julian",
            "email": " JULIAN@EXAMPLE.COM ",
            "address": {"city": "Medellin"},
            "company": {"name": "DevCodes"}
        }
    ]

    df = transform_users(users)

    assert len(df) == 1
    assert df.iloc[0]["name"] == "Julian Osorio"
    assert df.iloc[0]["email"] == "julian@example.com"
    assert df.iloc[0]["city"] == "Medellin"


def test_transform_empty_list():
    df = transform_users([])

    assert df.empty
    assert list(df.columns) == OUTPUT_COLUMNS


def test_transform_removes_empty_emails():
    users = [
        {
            "id": 1,
            "email": "   "
        },
        {
            "id": 2,
            "email": None
        }
    ]

    df = transform_users(users)

    assert df.empty


def test_transform_removes_duplicate_ids():
    users = [
        {"id": 1, "name": "Julian", "email": "julian@example.com"},
        {"id": 1, "name": "Another Julian", "email": "other@example.com"}
    ]

    df = transform_users(users)

    assert len(df) == 1
    assert df.iloc[0]["name"] == "Julian"


def test_transform_handles_missing_optional_fields():
    users = [
        {
            "id": 1,
            "email": "julian@example.com"
        }
    ]

    df = transform_users(users)

    assert len(df) == 1
    assert pd.isna(df.iloc[0]["city"])
    assert pd.isna(df.iloc[0]["company"])

