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

- API integration (HTTP GET requests to an external weather API)
- Data normalization (transforming raw API responses into structured records)
- Database persistence (storing normalized data in PostgreSQL)
- Dockerized databases (running PostgreSQL in a containerized environment)
- Transaction handling (understanding commits, rollbacks, and ACID principles)
- Error handling (implementing fail-safe exception handling)
- Retry and timeout handling (improving API resilience)
- Unit testing (validating transformation, extraction, configuration, and orchestration logic)
- CI/CD validation (running static analysis and unit tests with GitHub Actions)
- Environment configuration (externalizing application settings using `.env` variables)
- Operational troubleshooting (diagnosing runtime, database, CI/CD, and environment issues)

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

Developer Push
    ↓
GitHub Actions Workflow Triggered
    ↓
Python Environment Provisioned
    ↓
Project Dependencies Installed
    ↓
Pylint Static Analysis Executed
    ↓
Pytest Unit Tests Executed
    ↓
Branch Protection Quality Gates Applied

## Testing

This project uses `pytest` to validate pipeline behavior without requiring live API calls or database connections.

Current test coverage includes:

- Transform logic validation
- Unit conversion checks
- Environment configuration behavior
- API timeout and retry behavior
- Pipeline orchestration flow

Tests can be run locally with:

```bash
pytest
```

Static analysis can be run with:

```bash
pylint src tests utils
```

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

## Docker Compose Runtime

Phase 3 adds a containerized runtime using Docker Compose.

The Compose stack includes:

- PostgreSQL database container
- ETL application container
- Shared Docker network
- Persistent PostgreSQL volume
- Automatic schema initialization
- PostgreSQL healthcheck before ETL startup

Run the full stack:

```bash
docker compose up --build
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

## Project Status

### Phase 1 — Foundational ETL Pipeline

Phase 1 established the core ETL workflow and foundational data engineering concepts.

Completed capabilities:

- Open-Meteo API ingestion
- Data normalization and transformation
- PostgreSQL persistence
- Dockerized PostgreSQL runtime
- Environment-based configuration
- SQL schema design
- Operational troubleshooting basics

#### Phase 1 Architecture

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Open-Meteo API]:::api -->|HTTP JSON| B[Python ETL Pipeline]:::app
    B -->|Transform / Normalize| C[Structured Weather Record]:::process
    C -->|INSERT via psycopg2| D[(PostgreSQL Database)]:::db

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef process fill:#9467bd,color:#fff
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#9467bd,stroke-width:2px
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
```

### Phase 2 — Reliability and Testing Enhancements

Phase 2 focused on improving operational maturity, resiliency, testing, and CI/CD validation.

Completed capabilities:

- Retry and timeout handling
- Structured logging
- pytest-based unit testing
- Negative-path testing
- GitHub Actions CI validation
- Pipeline orchestration tests
- Reusable test fixtures
- Expanded troubleshooting documentation
- `pyproject.toml` centralized tooling configuration

#### Phase 2 Reliability and Testing Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[Developer Push]:::developer --> B[GitHub Actions Workflow]:::cicd
    B --> C[Install Dependencies]:::process
    C --> D[Pylint Static Analysis]:::validation
    D --> E[Pytest Unit Tests]:::testing
    E --> F[Retry / Timeout Logic Validation]:::resilience
    F --> G[Branch Protection Quality Gate]:::security

    classDef developer fill:#7f7f7f,color:#fff
    classDef cicd fill:#1f77b4,color:#fff
    classDef process fill:#ff7f0e,color:#000
    classDef validation fill:#d62728,color:#fff
    classDef testing fill:#9467bd,color:#fff
    classDef resilience fill:#17becf,color:#000
    classDef security fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#ff7f0e,stroke-width:2px
    linkStyle 2 stroke:#d62728,stroke-width:2px
    linkStyle 3 stroke:#9467bd,stroke-width:2px
    linkStyle 4 stroke:#17becf,stroke-width:2px
    linkStyle 5 stroke:#2ca02c,stroke-width:2px
```

### Phase 3 — Containerized Runtime and Orchestration

Phase 3 transitioned the project into a portable multi-service runtime using Docker and Docker Compose.

Completed capabilities:

- Dockerized ETL application runtime
- Docker Compose orchestration
- PostgreSQL healthchecks and startup readiness
- Persistent PostgreSQL volumes
- Automatic schema initialization
- Container networking and runtime configuration
- `.env` and `.env.example` externalized configuration strategy
- Makefile developer workflow automation
- Non-root container execution

#### Phase 3 Containerized Runtime

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Docker Compose]:::orchestrator --> B[ETL App Container]:::app
    A --> C[(PostgreSQL Container)]:::db
    B -->|DB_HOST=postgres<br/>DB_PORT=5432| C
    C --> D[(Persistent Volume)]:::storage
    E[schema.sql]:::config -->|Init on fresh volume| C
    C -->|Healthcheck / Readiness| B

    classDef orchestrator fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff
    classDef storage fill:#8c564b,color:#fff
    classDef config fill:#9467bd,color:#fff

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#1f77b4,stroke-width:2px
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
    linkStyle 3 stroke:#8c564b,stroke-width:2px
    linkStyle 4 stroke:#9467bd,stroke-width:2px
    linkStyle 5 stroke:#17becf,stroke-width:2px,stroke-dasharray: 5 5
```

### Phase 4 — Kubernetes Deployment Engineering

### Completed Phase 4 — Kubernetes Platform Deployment

Phase 4 focused on deploying the ETL pipeline into Kubernetes using native platform resources and operational workflows.

Completed capabilities include:

- Kubernetes namespace management
- PostgreSQL Kubernetes deployment
- Kubernetes Services and cluster DNS
- PersistentVolumeClaims
- ConfigMaps and Secrets
- Kubernetes Job-based ETL execution
- PostgreSQL schema initialization through ConfigMaps
- Kubernetes deployment runbooks
- Kubernetes troubleshooting documentation
- Runtime validation using `kubectl`
- Local Kubernetes image build workflows

#### Phase 4 Kubernetes Architecture

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Kubernetes Namespace]:::cluster --> B[ETL Kubernetes Job]:::job
    A --> C[(PostgreSQL Deployment)]:::db

    B -->|Cluster DNS<br/>postgres:5432| C

    D[ConfigMap]:::config --> B
    E[Secret]:::secret --> B

    F[PersistentVolumeClaim]:::storage --> C

    G[schema.sql ConfigMap]:::config --> C

    classDef cluster fill:#1f77b4,color:#fff
    classDef job fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff
    classDef config fill:#9467bd,color:#fff
    classDef secret fill:#d62728,color:#fff
    classDef storage fill:#8c564b,color:#fff

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#1f77b4,stroke-width:2px
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
    linkStyle 3 stroke:#9467bd,stroke-width:2px
    linkStyle 4 stroke:#d62728,stroke-width:2px
    linkStyle 5 stroke:#8c564b,stroke-width:2px
    linkStyle 6 stroke:#9467bd,stroke-width:2px
```

### Current State

The project now supports:

- Local Python ETL execution
- Dockerized PostgreSQL execution
- Fully containerized ETL runtime using Docker Compose
- Automated testing with pytest
- CI/CD validation with GitHub Actions
- Runtime configuration externalization using `.env`
- PostgreSQL healthchecks and startup readiness
- Operational troubleshooting and runtime diagnostics
- Kubernetes-native PostgreSQL deployment
- Kubernetes Services and cluster DNS
- Kubernetes ConfigMaps and Secrets
- Kubernetes PersistentVolumeClaims
- Kubernetes Job-based ETL execution
- Kubernetes operational workflows using `kubectl`
- Local Kubernetes platform deployment validation

### Next Phase — Helm and Kubernetes Packaging

Phase 5 will focus on improving Kubernetes deployment portability and operational maturity.

Planned Phase 5 enhancements include:

- Helm chart packaging
- Helm values-based configuration
- Kubernetes CronJobs
- Environment-specific deployment profiles
- Kubernetes observability foundations
- Metrics and monitoring integration
- Improved deployment automation
