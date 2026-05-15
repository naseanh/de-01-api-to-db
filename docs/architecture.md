# Architecture

## Overview

This project implements a simple, end-to-end ETL (Extract → Transform → Load) pipeline that ingests weather data from an external API and stores it in a PostgreSQL database.

The system is designed to demonstrate:

- Data ingestion from an external service
- Data transformation and normalization
- Persistent storage in a relational database
- Query-based data retrieval

## System Context

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Open-Meteo API]:::api -->|HTTP JSON| B[pipeline.py]:::app
    B ==>|INSERT via psycopg2| C[(PostgreSQL)]:::db

    D[DataGrip]:::tool -.->|Query| C
    C -->|Response| D

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff
    classDef tool fill:#aaaaaa,color:#000

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#2ca02c,stroke-width:3px
    linkStyle 2 stroke:#999999,stroke-dasharray: 5 5
    linkStyle 3 stroke:#555555,stroke-width:2px
```

## Description

- **Open-Meteo API**: External data source providing weather data
- **pipeline.py**: Core application responsible for ETL logic
- **PostgreSQL**: Persistent storage layer
- **DataGrip**: Tool used for querying and validating stored data

## ETL Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[Extract]:::step --> B[Transform]:::step
    B --> C[Load]:::step
    C --> D[(weather_observations table)]:::db

    classDef step fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#888888,stroke-width:1.5px
    linkStyle 1 stroke:#888888,stroke-width:1.5px
    linkStyle 2 stroke:#2ca02c,stroke-width:3px
```

## ETL Flow Description

1. Extract
    - Sends HTTP request to Open-Meteo API
    - Retrieves JSON payload
2. Transform
    - Extracts relevant fields
    - Converts units:
      - Celsius → Fahrenheit
      - km/h → mph
    - Normalizes data structure
3. Load
    - Inserts record into PostgreSQL
    - Uses ON CONFLICT to prevent duplicates

## Execution Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[run_pipeline]:::app --> B[extract]:::app
    B --> C[transform]:::app
    C --> D[load]:::app
    D --> E[(PostgreSQL)]:::db

    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#888888
    linkStyle 1 stroke:#888888
    linkStyle 2 stroke:#888888
    linkStyle 3 stroke:#2ca02c,stroke-width:3px
```

## Execution Flow Description

- `run_pipeline()` orchestrates execution
- Each function represents a distinct pipeline stage
- Data flows sequentially through the system

## Data Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Raw API JSON]:::api --> B[Parsed Data]:::app
    B:::app --> C[Transformed Record]:::app
    C --> D[(PostgreSQL Row)]:::db

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#1f77b4
    linkStyle 1 stroke:#ff7f0e
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
```

## Data Flow Description

- Raw API response is parsed into Python structures
- Data is transformed into a normalized record
- Record is inserted into the database

## Configuration Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[.env file] --> B[load_dotenv]
    B --> C[os.getenv]
    C --> D[DB_CONFIG / API_PARAMS]
    D --> E[pipeline.py execution]

    classDef config fill:#aaaaaa,color:#000
    classDef app fill:#ff7f0e,color:#000

    class A,B,C,D config
    class E app

    linkStyle 0 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 1 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 2 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 3 stroke:#bbbbbb,stroke-width:1.5px
```

## Configuration Flow Description

- Environment variables define runtime configuration
- Supports default + override pattern:
  - DEFAULT_* → fallback
  - WEATHER_* → runtime override

## Key Design Decisions

1. Environment-Based Configuration
    - Avoids hardcoding values
    - Enables flexible deployment
2. Idempotent Data Loading
    - UNIQUE (location, observed_at)
    - ON CONFLICT DO NOTHING
    - Prevents duplicate records
3. Separation of Concerns
    - Extract, Transform, Load are independent functions
    - Improves readability and maintainability
4. Context Managers for DB Access
    - Uses `with psycopg3.connect()` and `with conn.cursor()`
    - Ensures automatic cleanup of connections and cursors
    - Prevents resource leaks and connection exhaustion

## Kubernetes and Helm Runtime Architecture

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[GitHub Actions CI]:::ci -->|Deploy Package| B[Helm Chart]:::helm

    B -->|Templates| C[PostgreSQL Deployment]:::db
    B -->|Templates| D[ETL Job]:::job
    B -->|Templates| E[ETL CronJob]:::cron

    C -->|Persistent Storage| F[(PersistentVolumeClaim)]:::storage
    C -->|Cluster DNS| G[PostgreSQL Service]:::network

    D -->|postgres:5432| G
    E -->|postgres:5432| G

    H[Open-Meteo API]:::api -->|Weather JSON| D
    H -->|Scheduled Ingestion| E

    I[kubectl]:::tool -.->|Operations| C
    I -.->|Logs / Debugging| D
    I -.->|Scheduling Validation| E

    classDef api fill:#1f77b4,color:#fff
    classDef db fill:#2ca02c,color:#fff
    classDef storage fill:#8c564b,color:#fff
    classDef network fill:#17becf,color:#000
    classDef job fill:#ff7f0e,color:#000
    classDef cron fill:#d62728,color:#fff
    classDef helm fill:#9467bd,color:#fff
    classDef ci fill:#7f7f7f,color:#fff
    classDef tool fill:#aaaaaa,color:#000

    linkStyle 0 stroke:#9467bd,stroke-width:3px
    linkStyle 1 stroke:#9467bd,stroke-width:2px
    linkStyle 2 stroke:#9467bd,stroke-width:2px
    linkStyle 3 stroke:#9467bd,stroke-width:2px

    linkStyle 4 stroke:#8c564b,stroke-width:2px
    linkStyle 5 stroke:#17becf,stroke-width:2px

    linkStyle 6 stroke:#2ca02c,stroke-width:3px
    linkStyle 7 stroke:#d62728,stroke-width:3px

    linkStyle 8 stroke:#1f77b4,stroke-width:2px
    linkStyle 9 stroke:#1f77b4,stroke-width:2px

    linkStyle 10 stroke:#aaaaaa,stroke-width:2px,stroke-dasharray: 5 5
    linkStyle 11 stroke:#aaaaaa,stroke-width:2px,stroke-dasharray: 5 5
    linkStyle 12 stroke:#aaaaaa,stroke-width:2px,stroke-dasharray: 5 5
```

## Current Limitations

The platform has significantly evolved beyond the original standalone ETL implementation, but several limitations still exist.

Current limitations include:

- Single-region PostgreSQL deployment
- Single-node Kubernetes validation only
- No centralized logging stack
- No Prometheus metrics integration
- No Grafana dashboards
- No distributed tracing
- No connection pooling
- No horizontal scaling strategy for PostgreSQL
- No production ingress controller
- Local container registry dependency for Kubernetes image distribution
- Limited retry/backoff tuning for external API failures
- No advanced workload autoscaling
- No high-availability PostgreSQL configuration
- No centralized secret management solution
- No production-grade backup and disaster recovery workflows

## Possible Future Enhancements

### Data and Pipeline Enhancements

- Multi-location ingestion support
- Historical weather ingestion workflows
- Batch ingestion pipelines
- Incremental ingestion optimization
- Data retention and archival policies
- Data partitioning strategies for scale

### Platform and Kubernetes Enhancements

- Horizontal workload scaling
- Production-grade ingress controller support
- Kubernetes autoscaling
- Multi-environment deployment promotion workflows
- External container registry integration
- High-availability PostgreSQL deployment
- Advanced Helm deployment validation

### Observability and Monitoring Enhancements

- Prometheus metrics integration
- Grafana dashboard visualization
- OpenTelemetry instrumentation
- Distributed tracing
- Structured JSON logging
- Centralized log aggregation
- Alerting and operational diagnostics

### Application and API Enhancements

- REST API for querying weather data
- Authentication and authorization
- API rate limiting
- Query filtering and aggregation endpoints
- Swagger/OpenAPI documentation
- Background worker orchestration

### Operational and DevOps Enhancements

- Automated backup and restore workflows
- Disaster recovery procedures
- GitOps deployment workflows
- Advanced CI/CD deployment pipelines
- Security scanning and policy enforcement
- Infrastructure-as-Code integration
