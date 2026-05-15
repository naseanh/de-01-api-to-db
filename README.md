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
- Static analysis with pylint
- CI/CD validation with GitHub Actions
- Runtime configuration externalization using `.env`
- PostgreSQL healthchecks and startup readiness
- Operational troubleshooting and runtime diagnostics
- Kubernetes-native PostgreSQL deployment
- Kubernetes Services and cluster DNS
- Kubernetes ConfigMaps and Secrets
- Kubernetes PersistentVolumeClaims (PVCs)
- Kubernetes Job-based ETL execution
- Kubernetes CronJob-based scheduled ETL execution
- Kubernetes resource requests and limits
- Kubernetes operational workflows using `kubectl`
- Local Kubernetes platform deployment validation
- Helm chart packaging and templating
- Helm values-based configuration
- Helm environment deployment profiles
- Helm operational runbooks
- Helm release lifecycle management
- Helm deployment automation using Makefiles
- Helm chart validation within GitHub Actions

### Platform Tooling and Package Management Overview

| Platform / Ecosystem | Primary Tool | Purpose |
| --- | --- | --- |
| Python | `pip` | Python package and dependency management |
| Python Virtual Environments | `venv` | Isolated Python runtime environments |
| Docker | `docker` | Container runtime and image management |
| Docker Compose | `docker compose` | Multi-container local orchestration |
| Kubernetes | `kubectl` | Kubernetes cluster operations and management |
| Kubernetes Packaging | `helm` | Kubernetes application packaging and deployment |
| CI/CD | GitHub Actions | Automated validation and deployment workflows |
| PostgreSQL | `psql` | PostgreSQL database administration and querying |
| Static Analysis | `pylint` | Python code quality and linting |
| Testing | `pytest` | Python automated testing framework |
| Build Automation | `make` / `Makefile` | Operational workflow automation |
| Container Registry | Local Docker Registry | Kubernetes image distribution |
| Version Control | `git` | Source control and collaboration |
| Git Hosting | GitHub | Repository hosting and CI integration |

### Platform Evolution Diagram

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Python ETL<br/>Phase 1]:::python --> B[Testing + CI/CD<br/>Phase 2]:::ci
    B --> C[Docker Compose Runtime<br/>Phase 3]:::docker
    C --> D[Kubernetes Job Runtime<br/>Phase 4]:::k8s
    D --> E[Helm Packaging + CronJobs<br/>Phase 5]:::helm
    E -.-> F[Observability + Monitoring<br/>Phase 6]:::observe
    A1[pip / venv / psycopg2]:::tool --> A
    B1[pytest / pylint / GitHub Actions]:::tool --> B
    C1[Dockerfile / docker compose / .env]:::tool --> C
    D1[kubectl / ConfigMaps / Secrets / PVCs]:::tool --> D
    E1[Helm / values.yaml / Makefile]:::tool --> E
    F1[Prometheus / Grafana / OpenTelemetry]:::tool --> F

    classDef python fill:#ff7f0e,color:#000
    classDef ci fill:#9467bd,color:#fff
    classDef docker fill:#1f77b4,color:#fff
    classDef k8s fill:#2ca02c,color:#fff
    classDef helm fill:#17becf,color:#000
    classDef observe fill:#d62728,color:#fff
    classDef tool fill:#7f7f7f,color:#fff

    linkStyle 0 stroke:#9467bd,stroke-width:2px
    linkStyle 1 stroke:#1f77b4,stroke-width:2px
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
    linkStyle 3 stroke:#17becf,stroke-width:2px
    linkStyle 4 stroke:#d62728,stroke-width:2px,stroke-dasharray: 5 5
    linkStyle 5 stroke:#7f7f7f,stroke-width:1.5px,stroke-dasharray: 4 4
    linkStyle 6 stroke:#7f7f7f,stroke-width:1.5px,stroke-dasharray: 4 4
    linkStyle 7 stroke:#7f7f7f,stroke-width:1.5px,stroke-dasharray: 4 4
    linkStyle 8 stroke:#7f7f7f,stroke-width:1.5px,stroke-dasharray: 4 4
    linkStyle 9 stroke:#7f7f7f,stroke-width:1.5px,stroke-dasharray: 4 4
```

### Phase 5 — Helm Packaging and Kubernetes Operational Maturity

Phase 5 focuses on Kubernetes deployment portability, reusable infrastructure packaging, and operational automation.

Current Phase 5 capabilities include:

- Helm chart scaffold and deployment packaging
- Helm templating for PostgreSQL and ETL workloads
- Helm values-based runtime configuration
- Environment-specific values profiles
- Kubernetes CronJob support for scheduled ETL execution
- Kubernetes resource governance using requests and limits
- Helm deployment automation via Makefile targets
- Helm operational runbooks and troubleshooting workflows
- Helm NOTES.txt operational guidance
- GitHub Actions Helm validation and rendering tests

Planned upcoming enhancements include:

- Kubernetes observability foundations
- Metrics and monitoring integration
- Helm test hooks
- Advanced deployment validation workflows
- Kubernetes scaling and resiliency concepts
- Production-grade container registry workflows
- Centralized logging and telemetry integration

### Next Phase — Observability and Platform Monitoring

Phase 6 will focus on observability, telemetry, monitoring, and production-grade operational visibility across the ETL platform.

Planned Phase 6 enhancements include:

- Prometheus metrics integration
- Grafana dashboards and visualization
- Kubernetes metrics collection
- Application-level telemetry instrumentation
- Structured logging improvements
- Centralized logging workflows
- OpenTelemetry (OTel) foundations
- Kubernetes health and performance monitoring
- Alerting and operational diagnostics
- Resource utilization analysis
- Platform troubleshooting dashboards
- Observability-focused CI/CD validation
- Production-style monitoring architecture
- Metrics-driven operational analysis
