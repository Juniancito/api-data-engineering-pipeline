
from src.transform import transform_users


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
