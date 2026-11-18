
from unittest.mock import MagicMock, call, patch

from src.extract import create_http_session


@patch("src.extract.HTTPAdapter")
@patch("src.extract.requests.Session")
def test_create_http_session(mock_session_factory, mock_adapter_factory):
    mock_session = MagicMock()
    mock_adapter = MagicMock()

    mock_session_factory.return_value = mock_session
    mock_adapter_factory.return_value = mock_adapter

    result = create_http_session()

    assert result is mock_session

    mock_adapter_factory.assert_called_once()
    mock_session.mount.assert_has_calls([
        call("http://", mock_adapter),
        call("https://", mock_adapter)
    ])

    retry_strategy = mock_adapter_factory.call_args.kwargs["max_retries"]

    assert retry_strategy.total == 3
    assert retry_strategy.connect == 3
    assert retry_strategy.read == 3
    assert retry_strategy.status == 3
    assert retry_strategy.backoff_factor == 1
    assert retry_strategy.backoff_jitter == 0.3
    assert retry_strategy.status_forcelist == [
    429, 500, 502, 503, 504
    ]
    assert retry_strategy.allowed_methods == ["GET"]
    assert retry_strategy.respect_retry_after_header is True
