
import os

import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


@pytest.fixture(scope="session")
def integration_database_url():
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        pytest.fail(
            f"Integration database is unavailable: {exc}"
        )
    finally:
        engine.dispose()

    return database_url


@pytest.fixture
def db_engine(integration_database_url):
    engine = create_engine(integration_database_url)

    def clean_database():
        with engine.begin() as connection:
            connection.execute(
                text("DROP TABLE IF EXISTS rejected_users")
            )
            connection.execute(
                text("DROP TABLE IF EXISTS pipeline_runs")
            )
            connection.execute(
                text("DROP TABLE IF EXISTS users")
            )

    clean_database()

    yield engine

    clean_database()
    engine.dispose()
