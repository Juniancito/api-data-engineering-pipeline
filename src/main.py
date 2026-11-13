import os
import logging

from dotenv import load_dotenv

from src.extract import extract_users
from src.validation import validate_users
from src.transform import transform_users
from src.load import load_users

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

    logger.info("Starting ETL process - Pipeline")

    # Extract
    raw_users = extract_users(api_url)
    logger.info(f"Extracted {len(raw_users)} users from API.")

    #Validate
    valid_users, rejected_users = validate_users(raw_users)
    logger.info("validated users: %d", len(valid_users))
    logger.warning("rejected users: %d", len(rejected_users))

    #Transform
    transformed_users = transform_users(valid_users)
    logger.info(f"Transformed users into DataFrame with {len(transformed_users)} records.")

    #Load
    loaded = load_users(transformed_users, database_url)
    logger.info(f"Loaded {loaded} users into the database.")

    logger.info("ETL process completed successfully.")

if __name__ == "__main__":
    main()