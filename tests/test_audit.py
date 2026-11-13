
from unittest.mock import MagicMock, patch

import pytest

from src.audit import start_pipeline_run, finish_pipeline_run


RUN_ID = "123e4567-e89b-12d3-a456-426614174000"
DATABASE_URL = "postgresql://test:test@localhost/test"


@patch("src.audit.create_engine")
def test_start_pipeline_run(mock_create_engine):
    engine = MagicMock()
    connection = MagicMock()

    mock_create_engine.return_value = engine
    engine.begin.return_value.__enter__.return_value = connection

    start_pipeline_run(RUN_ID, DATABASE_URL)

    assert connection.execute.call_count == 2
    engine.dispose.assert_called_once()


@patch("src.audit.create_engine")
def test_finish_pipeline_run(mock_create_engine):
    engine = MagicMock()
    connection = MagicMock()

    mock_create_engine.return_value = engine
    engine.begin.return_value.__enter__.return_value = connection

    result = MagicMock()
    result.rowcount = 1
    connection.execute.return_value = result

    finish_pipeline_run(
        RUN_ID,
        DATABASE_URL,
        "SUCCESS",
        records_extracted=10,
        records_valid=10,
        records_rejected=0,
        records_transformed=10,
        records_loaded=10
    )

    connection.execute.assert_called_once()
    engine.dispose.assert_called_once()


@patch("src.audit.create_engine")
def test_finish_pipeline_run_not_found(mock_create_engine):
    engine = MagicMock()
    connection = MagicMock()

    mock_create_engine.return_value = engine
    engine.begin.return_value.__enter__.return_value = connection

    result = MagicMock()
    result.rowcount = 0
    connection.execute.return_value = result

    with pytest.raises(RuntimeError, match="Pipeline run not found"):
        finish_pipeline_run(
            RUN_ID,
            DATABASE_URL,
            "SUCCESS"
        )

    engine.dispose.assert_called_once()


def test_finish_pipeline_run_invalid_status():
    with pytest.raises(ValueError, match="Invalid final pipeline status"):
        finish_pipeline_run(
            RUN_ID,
            DATABASE_URL,
            "UNKNOWN"
        )
