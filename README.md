
# API Data Engineering Pipeline

End-to-end ETL pipeline built with Python, PostgreSQL and Docker, designed with data validation, auditability, automated testing and continuous integration.

## Overview

This project implements an ETL pipeline that extracts user data from a REST API, validates and transforms records, handles rejected data, and loads the resulting information into PostgreSQL.

The pipeline also tracks execution metrics and maintains an audit history for each run.

## Architecture

```text
                 REST API
                    |
                    v
               EXTRACTION
                    |
                    v
                VALIDATION
                 /      \
                /        \
        VALID RECORDS   REJECTED RECORDS
               |              |
               v              v
          TRANSFORMATION   PERSISTENCE
               |
               v
              LOAD
               |
               v
           PostgreSQL
               |
               v
         PIPELINE AUDIT
```

## Technologies

- Python 3.11
- Pandas
- Requests
- Pydantic
- SQLAlchemy
- PostgreSQL 16
- Docker Compose
- Pytest
- Pytest-Cov
- Ruff
- GitHub Actions

## Features

- REST API data extraction.
- HTTP retry strategy for transient failures.
- Data validation using Pydantic.
- Rejected records management.
- Data cleaning and normalization with Pandas.
- Idempotent database loading using UPSERT.
- PostgreSQL persistence.
- Pipeline execution auditing.
- Execution metrics and error tracking.
- Unit and integration testing.
- Automated code quality checks with Ruff.
- Continuous integration with GitHub Actions.
- Test coverage enforcement.

## Project Structure

```text
api-data-engineering-pipeline/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── sql/
│
├── src/
│   ├── audit.py
│   ├── extract.py
│   ├── load.py
│   ├── main.py
│   ├── rejected.py
│   ├── schemas.py
│   ├── transform.py
│   └── validation.py
│
├── tests/
│   ├── integration/
│   ├── test_audit.py
│   ├── test_extract.py
│   ├── test_extract_session.py
│   ├── test_main.py
│   ├── test_rejected.py
│   ├── test_transformation.py
│   └── test_validation.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── requirements-dev.txt
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11
- Docker Desktop
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/Juniancito/api-data-engineering-pipeline.git

cd api-data-engineering-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Configure environment variables:

```powershell
Copy-Item .env.example .env
```

Review the values in `.env` before running the pipeline.

## Database Setup

Start PostgreSQL containers:

```bash
docker compose up -d
```

The project provides two PostgreSQL databases:

| Database | Port | Purpose |
|---|---:|---|
| data_engineering | 5432 | Main pipeline |
| data_engineering_test | 5433 | Integration testing |

## Run the Pipeline

```bash
python -m src.main
```

## Testing

Run all tests:

```bash
python -m pytest -v
```

Run code quality checks:

```bash
ruff check .
```

Run tests with coverage:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

Enforce a minimum coverage of 90%:

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

## Continuous Integration

GitHub Actions automatically executes the following checks on pushes and pull requests targeting `main`:

1. Install project dependencies.
2. Run Ruff code quality checks.
3. Execute unit and integration tests.
4. Generate test coverage reports.
5. Enforce a minimum coverage threshold of 90%.

## Author

Julian Osorio
