
from unittest.mock import Mock, patch

import pytest
import requests

from src.extract import extract_users


@patch("src.extract.create_http_session")
def test_extract_users_success(mock_session_factory):
    mock_session = Mock()
    mock_session_factory.return_value.__enter__.return_value = mock_session

    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "name": "Julian"}
    ]

    mock_session.get.return_value = mock_response

    result = extract_users("https://example.com/users")

    assert len(result) == 1
    assert result[0]["id"] == 1


@patch("src.extract.create_http_session")
def test_extract_users_http_error(mock_session_factory):
    mock_session = Mock()
    mock_session_factory.return_value.__enter__.return_value = mock_session

    mock_session.get.side_effect = requests.ConnectionError(
        "Connection failed"
    )

    with pytest.raises(RuntimeError, match="Failed to extract"):
        extract_users("https://example.com/users")


@patch("src.extract.create_http_session")
def test_extract_users_invalid_response(mock_session_factory):
    mock_session = Mock()
    mock_session_factory.return_value.__enter__.return_value = mock_session

    mock_response = Mock()
    mock_response.json.return_value = {"error": "Invalid response"}

    mock_session.get.return_value = mock_response

    with pytest.raises(ValueError, match="Expected a list"):
        extract_users("https://example.com/users")
