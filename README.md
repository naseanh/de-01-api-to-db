# API to PostgreSQL ETL Pipeline

## Overview

This project implements a basic ETL (Extract → Transform → Load) pipeline that:

- Extracts real-time weather data from the Open-Meteo API
- Transforms and normalizes the data (including unit conversions)
- Loads the data into a PostgreSQL database

This project demonstrates foundational data engineering concepts such as:

- API ingestion
- Data transformation
- Database schema design
- Idempotent data loading
- Environment-based configuration

## Key Concepts Practiced

- API integration (HTTP GET requests to external weather API)
- Data normalization (transforming raw API responses into structured records)
- Database persistence (storing normalized data in PostgreSQL)
- Dockerized databases (running PostgreSQL in a containerized environment)
- Transaction handling (understanding commits, rollbacks, and ACID principles)
- Error handling (implementing fail-safe exception handling)
- Environment configuration (externalizing application settings using .env variables)
- Operational troubleshooting (diagnosing runtime, database, and environment issues)

## Tech Stack

- Python
- requests (HTTP client)
- psycopg2 (PostgreSQL adapter)
- PostgreSQL (database)
- Docker (local DB container)
- DataGrip (query tool)
- python-dotenv (configuration management)

## Architecture

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Open-Meteo API]:::api -->|HTTP JSON| B[pipeline.py]:::app
    B ==>|INSERT via psycopg2| C[(PostgreSQL)]:::db

    D[DataGrip / CLI]:::tool -.->|Query| C
    C -->|Response| D

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff
    classDef tool fill:#aaaaaa,color:#000

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#2ca02c,stroke-width:2px
    linkStyle 2 stroke:#999999,stroke-dasharray: 5 5
    linkStyle 3 stroke:#999999,stroke-width:2px
```

## CI/CD Workflow

This repository uses GitHub Actions to automatically validate code changes during development.

Current workflow capabilities include:

- Automatic workflow execution on push events
- Python environment provisioning
- Dependency installation
- Static code analysis using pylint
- Branch protection enforcement before merge

### Workflow Overview

```text
Developer Push
    ↓
GitHub Actions Workflow Triggered
    ↓
Python Environment Provisioned
    ↓
Project Dependencies Installed
    ↓
Static Analysis Executed
    ↓
Branch Protection Quality Gates Applied
```

## Quick Start

1. Activate virtual environment

    ```bash
    source .venv/bin/activate
    ```

2. Start PostgeSQL

    ```bash
    docker start pipeline_postgres
    ```

3. Run Schema

    ```bash
    psql -h localhost -p 5433 -U pipeline_user -d pipeline_db -f sql/schema.sql
    ```

4. Run pipeline

    ```bash
    python3 src/pipeline.py
    ```

## Example Queries

See [queries](sql/queries.sql) for:

- Latest observations
- Location filtering
- Time-based quries
- Aggregations
- Data validation queries

## Documentation

- [Architecture](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [Data Model](docs/data-model.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Retrospective](docs/phase-1-retrospective.md)

## Example Output

```bash
Pipeline complete. Location: Augusta, GA | Temp: 22.6C / 72.7F | Wind: 15.2 km/h / 9.4 mph | Observed: 2026-04-23 23:00:00
```

## Next Steps (Phase 2)

Planned Phase 2 enhancements include:

- Retry and timeout handling
- Structured logging
- Unit testing with pytest
- Enhanced CI/CD workflows
- Security scanning
- Containerized application deployment
- Metrics and observability
- Kubernetes deployment exploration
