
from unittest.mock import MagicMock

import pytest

import src.main as pipeline


def configure_environment(monkeypatch):
    monkeypatch.setattr(pipeline, "load_dotenv", MagicMock())

    monkeypatch.setenv("API_URL", "https://example.com/users")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost/test"
    )


@pytest.mark.parametrize(
    ("rejected_users", "expected_status"),
    [
        ([], "SUCCESS"),
        ([{"record_index": 1}], "PARTIAL")
    ]
)
def test_main_success(
    monkeypatch,
    rejected_users,
    expected_status
):
    configure_environment(monkeypatch)

    pipeline_run_id = "test-run-123"

    monkeypatch.setattr(
        pipeline,
        "uuid4",
        lambda: pipeline_run_id
    )

    start_mock = MagicMock()
    finish_mock = MagicMock()

    monkeypatch.setattr(pipeline, "start_pipeline_run", start_mock)
    monkeypatch.setattr(pipeline, "finish_pipeline_run", finish_mock)

    monkeypatch.setattr(
        pipeline,
        "extract_users",
        lambda url: [{"id": 1}, {"id": 2}]
    )

    monkeypatch.setattr(
        pipeline,
        "validate_users",
        lambda users: ([{"id": 1}], rejected_users)
    )

    persist_mock = MagicMock()
    monkeypatch.setattr(
        pipeline,
        "persist_rejected_users",
        persist_mock
    )

    monkeypatch.setattr(
        pipeline,
        "transform_users",
        lambda users: [{"id": 1}]
    )

    monkeypatch.setattr(
        pipeline,
        "load_users",
        lambda users, database_url: 1
    )

    pipeline.main()

    start_mock.assert_called_once_with(
        pipeline_run_id,
        "postgresql://postgres:postgres@localhost/test"
    )

    persist_mock.assert_called_once()

    finish_mock.assert_called_once()

    assert finish_mock.call_args.args == (
        pipeline_run_id,
        "postgresql://postgres:postgres@localhost/test",
        expected_status
    )

    assert finish_mock.call_args.kwargs == {
        "records_extracted": 2,
        "records_valid": 1,
        "records_rejected": len(rejected_users),
        "records_transformed": 1,
        "records_loaded": 1
    }


def test_main_missing_environment_variables(monkeypatch):
    monkeypatch.setattr(pipeline, "load_dotenv", MagicMock())

    monkeypatch.delenv("API_URL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValueError, match="Missing Env configuration"):
        pipeline.main()


def test_main_pipeline_failure(monkeypatch):
    configure_environment(monkeypatch)

    monkeypatch.setattr(
        pipeline,
        "uuid4",
        lambda: "test-run-123"
    )

    start_mock = MagicMock()
    finish_mock = MagicMock()

    monkeypatch.setattr(pipeline, "start_pipeline_run", start_mock)
    monkeypatch.setattr(pipeline, "finish_pipeline_run", finish_mock)

    monkeypatch.setattr(
        pipeline,
        "extract_users",
        MagicMock(side_effect=RuntimeError("API unavailable"))
    )

    with pytest.raises(RuntimeError, match="API unavailable"):
        pipeline.main()

    finish_mock.assert_called_once()

    assert finish_mock.call_args.args == (
        "test-run-123",
        "postgresql://postgres:postgres@localhost/test",
        "FAILED"
    )

    assert finish_mock.call_args.kwargs["error_message"] == "API unavailable"


def test_main_failure_audit_error(monkeypatch):
    configure_environment(monkeypatch)

    monkeypatch.setattr(
        pipeline,
        "uuid4",
        lambda: "test-run-123"
    )

    monkeypatch.setattr(
        pipeline,
        "start_pipeline_run",
        MagicMock()
    )

    monkeypatch.setattr(
        pipeline,
        "extract_users",
        MagicMock(side_effect=RuntimeError("Original pipeline error"))
    )

    monkeypatch.setattr(
        pipeline,
        "finish_pipeline_run",
        MagicMock(side_effect=RuntimeError("Audit database unavailable"))
    )

    with pytest.raises(
        RuntimeError,
        match="Original pipeline error"
    ):
        pipeline.main()
