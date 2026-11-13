from sqlalchemy import create_engine, text

CREATE_PIPELINE_RUNS_TABLE = text("""
    CREATE TABLE IF NOT EXISTS pipeline_runs(
        pipeline_run_id UUID PRIMARY KEY,
        STATUS varchar(20) NOT NULL
            CHECK (status IN ('RUNNING', 'SUCCESS', 'PARTIAL', 'FAILED')),
            started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            finished_at TIMESTAMPTZ,
            records_extracted INTEGER NOT NULL DEFAULT 0,
            records_valid INTEGER NOT NULL DEFAULT 0,
            records_rejected INTEGER NOT NULL DEFAULT 0,
            records_transformed INTEGER NOT NULL DEFAULT 0,
            records_loaded INTEGER NOT NULL DEFAULT 0,
            error_message TEXT
        );
""")


INSERT_PIPELINE_RUN = text("""
    INSERT INTO pipeline_runs (pipeline_run_id, status)
    VALUES (CAST(:pipeline_run_id AS UUID), 'RUNNING');
""")

UPDATE_PIPELINE_RUN = text("""
    UPDATE pipeline_runs
    SET
        status = :status,
        finished_at = CURRENT_TIMESTAMP,
        records_extracted = :records_extracted,
        records_valid = :records_valid,
        records_rejected = :records_rejected,
        records_transformed = :records_transformed,
        records_loaded = :records_loaded,
        error_message = :error_message
    WHERE pipeline_run_id = CAST(:pipeline_run_id AS UUID);
""")

def start_pipeline_run(
        pipeline_run_id: str,
        database_url: str
) -> None:

    """
        Register a new pipeline execution
    """

    engine = create_engine(database_url)

    try:
        with engine.begin() as connection:
            connection.execute(CREATE_PIPELINE_RUNS_TABLE)
            connection.execute(
                INSERT_PIPELINE_RUN,
                {"pipeline_run_id": pipeline_run_id}
            )
    finally:
        engine.dispose()


def finish_pipeline_run(
    pipeline_run_id: str,
    database_url: str,
    status: str,
    records_extracted: int = 0,
    records_valid: int = 0,
    records_rejected: int = 0,
    records_transformed: int = 0,
    records_loaded: int = 0,
    error_message: str | None = None
) -> None:
    """Update the final state and metrics of a pipeline execution."""

    allowed_statuses = {"SUCCESS", "PARTIAL", "FAILED"}

    if status not in allowed_statuses:
        raise ValueError(f"Invalid final pipeline status: {status}. Must be one of {allowed_statuses}")

    engine = create_engine(database_url)

    try:
        with engine.begin() as connection:
            result = connection.execute(
                UPDATE_PIPELINE_RUN,
                {
                    "pipeline_run_id": pipeline_run_id,
                    "status": status,
                    "records_extracted": records_extracted,
                    "records_valid": records_valid,
                    "records_rejected": records_rejected,
                    "records_transformed": records_transformed,
                    "records_loaded": records_loaded,
                    "error_message": error_message
                }
            )

            if result.rowcount != 1:
                raise RuntimeError(
                    f"Pipeline run not found: {pipeline_run_id}"
                )
    finally:
        engine.dispose()        