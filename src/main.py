
import os
import logging

from uuid import uuid4
from dotenv import load_dotenv

from src.extract import extract_users
from src.validation import validate_users
from src.transform import transform_users
from src.load import load_users
from src.rejected import persist_rejected_users


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    api_url = os.getenv("API_URL")
    database_url = os.getenv("DATABASE_URL")

    if not api_url or not database_url:
        raise ValueError("Missing Env configuration")

    pipeline_run_id = str(uuid4())

    logger.info(
        "Starting ETL pipeline. Run ID: %s",
        pipeline_run_id
    )

    # Extract
    raw_users = extract_users(api_url)

    logger.info(
        "Extracted users: %d",
        len(raw_users)
    )

    # Validate
    valid_users, rejected_users = validate_users(raw_users)

    logger.info(
        "Validated users: %d",
        len(valid_users)
    )

    logger.warning(
        "Rejected users: %d",
        len(rejected_users)
    )

    # Persist rejected records
    persisted_rejected = persist_rejected_users(
        rejected_users,
        pipeline_run_id,
        database_url
    )

    logger.info(
        "Persisted rejected users: %d",
        persisted_rejected
    )

    # Transform
    transformed_users = transform_users(valid_users)

    logger.info(
        "Transformed users: %d",
        len(transformed_users)
    )

    # Load
    loaded = load_users(
        transformed_users,
        database_url
    )

    logger.info(
        "Loaded users into database: %d",
        loaded
    )

    logger.info(
        "ETL process completed. Run ID: %s",
        pipeline_run_id
    )


if __name__ == "__main__":
    main()
