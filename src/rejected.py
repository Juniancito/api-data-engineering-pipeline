import json

from sqlalchemy import create_engine, text

CREATE_REJECTED_TABLE = text("""
    CREATE TABLE IF NOT EXISTS rejected_users (
        id BIGSERIAL PRIMARY KEY,
        pipeline_run_id UUID NOT NULL,
        record_index INTEGER NOT NULL,
        record_data JSONB NOT NULL,
        validation_errors JSONB NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
""")

INSERT_REJECTED_USER = text("""
        INSERT INTO rejected_users (
        pipeline_run_id,
        record_index,
        record_data,
        validation_errors
    )
    VALUES (
        CAST(:pipeline_run_id AS UUID),
        :record_index,
        CAST(:record_data AS JSONB),
        CAST(:validation_errors AS JSONB)
    );
"""
)

def persist_rejected_users(
    rejected_users: list[dict],
    pipeline_run_id: str,
    database_url: str
) -> int:
    """
    Persist rejected user records to the database.

    Args:
        rejected_users (list[dict]): List of rejected user records.
        pipeline_run_id (str): Unique identifier for the current pipeline run.
        database_url (str): Database connection URL.

    Returns:
        int: Number of rejected records persisted.
    """

    engine = create_engine(database_url)

    records = [
        {
            "pipeline_run_id": pipeline_run_id,
            "record_index": rejected["record_index"],
            "record_data": json.dumps(rejected["record_data"]),
            "validation_errors": json.dumps(rejected["errors"]),
        }
        for rejected in rejected_users
    ]

    try:
        with engine.begin() as connection:
            connection.execute(CREATE_REJECTED_TABLE)

            if records:
                connection.execute(INSERT_REJECTED_USER, records)

        return len(records)

    finally:
        engine.dispose()
