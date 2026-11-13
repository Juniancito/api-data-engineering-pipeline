
from unittest.mock import MagicMock, patch

from src.rejected import persist_rejected_users


@patch("src.rejected.create_engine")
def test_persist_rejected_users(mock_create_engine):
    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_engine.begin.return_value.__enter__.return_value = mock_connection

    rejected_users = [
        {
            "record_index": 0,
            "record_data": {
                "id": 1,
                "email": "invalid-email"
            },
            "errors": [
                {
                    "type": "value_error",
                    "loc": ["email"],
                    "msg": "Invalid email address"
                }
            ]
        }
    ]

    result = persist_rejected_users(
        rejected_users,
        "postgresql://test:test@localhost/test",
        "123e4567-e89b-12d3-a456-426614174000"
    )

    assert result == 1
    assert mock_connection.execute.call_count == 2
    mock_engine.dispose.assert_called_once()


@patch("src.rejected.create_engine")
def test_persist_rejected_users_empty(mock_create_engine):
    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_engine.begin.return_value.__enter__.return_value = mock_connection

    result = persist_rejected_users(
        [],
        "postgresql://test:test@localhost/test",
        "123e4567-e89b-12d3-a456-426614174000"
    )

    assert result == 0
    assert mock_connection.execute.call_count == 1
    mock_engine.dispose.assert_called_once()
