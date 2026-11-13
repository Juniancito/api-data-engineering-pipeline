# api-data-engineering-pipeline
end-to-end ETL pipeline using Python, PostgreSQL and Docker



# API Data Engineering Pipeline

End-to-end ETL pipeline using Python, PostgreSQL and Docker.

## Overview

This project extracts users data from a REST API,
transforms and normalizes the information using Pandas,
and loads it into PostgreSQL.

## Architecture

API -> Extract -> Transform -> Load -> PostgreSQL

## Technologies

- Python 3.12
- Pandas
- Requests
- SQLAlchemy
- PostgreSQL 16
- Docker
- Pytest

## Features

- REST API data extraction
- Data normalization and cleaning
- Idempotent data loading (UPSERT)
- PostgreSQL persistence
- Unit testing
- Dockerized database

## Execution

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install requirements.
4. Configure the .env file.
5. Start PostgreSQL with Docker Compose.
6. Run the pipeline.

```bash
pip install -r requirements.txt
docker compose up -d
python -m src.main
```

## Author

Julian Osorio
