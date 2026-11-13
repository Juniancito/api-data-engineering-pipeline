
from src.validation import validate_users


def test_validate_valid_user():
    users = [
        {
            "id": 1,
            "name": "Julian Osorio",
            "username": "julian",
            "email": "julian@example.com",
            "address": {"city": "Medellin"},
            "company": {"name": "DevCodes"}
        }
    ]

    valid, rejected = validate_users(users)

    assert len(valid) == 1
    assert len(rejected) == 0
    assert valid[0]["id"] == 1
    assert valid[0]["address"]["city"] == "Medellin"


def test_validate_invalid_email():
    users = [
        {
            "id": 1,
            "email": "invalid-email"
        }
    ]

    valid, rejected = validate_users(users)

    assert len(valid) == 0
    assert len(rejected) == 1


def test_validate_invalid_id():
    users = [
        {
            "id": -1,
            "email": "julian@example.com"
        }
    ]

    valid, rejected = validate_users(users)

    assert len(valid) == 0
    assert len(rejected) == 1


def test_validate_missing_required_email():
    users = [
        {
            "id": 1,
            "name": "Julian"
        }
    ]

    valid, rejected = validate_users(users)

    assert len(valid) == 0
    assert len(rejected) == 1


def test_validate_optional_fields():
    users = [
        {
            "id": 1,
            "email": "julian@example.com"
        }
    ]

    valid, rejected = validate_users(users)

    assert len(valid) == 1
    assert len(rejected) == 0
    assert valid[0]["address"] is None
