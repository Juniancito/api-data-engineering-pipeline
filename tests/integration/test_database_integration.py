
import pandas as pd
from uuid import uuid4

from sqlalchemy import text

from src.audit import (
    start_pipeline_run,
    finish_pipeline_run
)
from src.rejected import persist_rejected_users
from src.load import load_users


def test_pipeline_audit_and_rejected_records(db_engine, integration_database_url):
    database_url = integration_database_url
    pipeline_run_id = str(uuid4())

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

    # 1. Start pipeline execution
    start_pipeline_run(
        pipeline_run_id,
        database_url
    )

    # 2. Persist rejected records
    rejected_count = persist_rejected_users(
        rejected_users,
        pipeline_run_id,
        database_url
    )

    # 3. Finish pipeline execution
    finish_pipeline_run(
        pipeline_run_id,
        database_url,
        "PARTIAL",
        records_extracted=10,
        records_valid=9,
        records_rejected=1,
        records_transformed=9,
        records_loaded=9
    )

    # 4. Verify audit record
    with db_engine.connect() as connection:
        run = connection.execute(
            text("""
                SELECT *
                FROM pipeline_runs
                WHERE pipeline_run_id = :run_id
            """),
            {"run_id": pipeline_run_id}
        ).mappings().one()

        rejected = connection.execute(
            text("""
                SELECT *
                FROM rejected_users
                WHERE pipeline_run_id = :run_id
            """),
            {"run_id": pipeline_run_id}
        ).mappings().one()

    assert rejected_count == 1

    assert run["status"] == "PARTIAL"
    assert run["records_extracted"] == 10
    assert run["records_valid"] == 9
    assert run["records_rejected"] == 1
    assert run["records_transformed"] == 9
    assert run["records_loaded"] == 9
    assert run["finished_at"] is not None

    assert rejected["record_index"] == 0
    assert rejected["record_data"]["email"] == "invalid-email"


def test_load_users_upsert(db_engine, integration_database_url):
    database_url = integration_database_url

    first_batch = pd.DataFrame([
        {
            "user_id": 1,
            "name": "Julian",
            "username": "julian",
            "email": "old@example.com",
            "city": "Medellin",
            "company": "DevCodes"
        }
    ])

    second_batch = pd.DataFrame([
        {
            "user_id": 1,
            "name": "Julian Osorio",
            "username": "julian",
            "email": "new@example.com",
            "city": "El Penol",
            "company": "DevCodes"
        }
    ])

    # 1. Insert first record
    first_loaded = load_users(
        first_batch,
        database_url
    )

    # 2. Update existing record
    second_loaded = load_users(
        second_batch,
        database_url
    )

    # 3. Verify database state
    with db_engine.connect() as connection:
        users = connection.execute(
            text("""
                SELECT *
                FROM users
                WHERE user_id = 1
            """)
        ).mappings().all()

    assert first_loaded == 1
    assert second_loaded == 1

    # There must be only one record.
    assert len(users) == 1

    # The record must contain the updated information.
    assert users[0]["name"] == "Julian Osorio"
    assert users[0]["email"] == "new@example.com"
    assert users[0]["city"] == "El Penol"
