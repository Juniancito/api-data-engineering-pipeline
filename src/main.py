
import os
import logging

from uuid import uuid4
from dotenv import load_dotenv

from src.extract import extract_users
from src.validation import validate_users
from src.transform import transform_users
from src.load import load_users
from src.rejected import persist_rejected_users
from src.audit import start_pipeline_run, finish_pipeline_run


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

    metrics = {
        "records_extracted": 0,
        "records_valid": 0,
        "records_rejected": 0,
        "records_transformed": 0,
        "records_loaded": 0
    }

    start_pipeline_run(pipeline_run_id, database_url)

    logger.info(
        "Pipeline started. Run ID: %s",
        pipeline_run_id
    )

    try:
        # Extract
        raw_users = extract_users(api_url)
        metrics["records_extracted"] = len(raw_users)

        # Validate
        valid_users, rejected_users = validate_users(raw_users)

        metrics["records_valid"] = len(valid_users)
        metrics["records_rejected"] = len(rejected_users)

        # Persist rejected records
        persist_rejected_users(
            rejected_users,
            pipeline_run_id,
            database_url
        )

        # Transform
        transformed_users = transform_users(valid_users)

        metrics["records_transformed"] = len(transformed_users)

        # Load
        loaded = load_users(transformed_users, database_url)

        metrics["records_loaded"] = loaded

        final_status = (
            "PARTIAL" if rejected_users else "SUCCESS"
        )

        finish_pipeline_run(
            pipeline_run_id,
            database_url,
            final_status,
            **metrics
        )

        logger.info(
            "Pipeline completed. Status: %s | Metrics: %s | Run ID: %s",
            final_status,
            metrics,
            pipeline_run_id
        )

    except Exception as exc:
        logger.exception(
            "Pipeline execution failed. Run ID: %s",
            pipeline_run_id
        )

        try:
            finish_pipeline_run(
                pipeline_run_id,
                database_url,
                "FAILED",
                error_message=str(exc),
                **metrics
            )
        except Exception:
            logger.exception(
                "Could not persist pipeline failure audit. Run ID: %s",
                pipeline_run_id
            )

        raise


if __name__ == "__main__":
    main()
