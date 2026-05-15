# Phase 1 Retrospective — API to PostgreSQL ETL Pipeline

## Overview

This phase focused on building a foundational ETL (Extract, Transform, Load) pipeline using Python, PostgreSQL, Docker, and a public weather API.

The goal was to gain hands-on experience with:

- API integration (HTTP GET requests to external weather API)
- Data normalization (transforming raw API responses into structured records)
- Database persistence (storing normalized data in PostgreSQL)
- Dockerized databases (running PostgreSQL in a containerized environment)
- Transaction handling (understanding commits, rollbacks, and ACID principles)
- Error handling (implementing fail-safe exception handling)
- Environment configuration (externalizing application settings using .env variables)
- Operational troubleshooting (diagnosing runtime, database, and environment issues)

## Objectives

### Completed Objectives

- Successfully connected to external weather API
- Extracted JSON weather data
- Transformed API response into normalized schema
- Loaded records into PostgreSQL
- Containerized PostgreSQL with Docker
- Added environment-based configuration using `.env`
- Implemented idempotent inserts with ON CONFLICT
- Practiced transaction and failure testing

## Architecture Summary

### Components

| Component | Purpose |
| --------- | --------- |
| Python | ETL orchestration |
| requests | API communication |
| psycopg2 | PostgreSQL connectivity |
| PostgreSQL | Persistent storage |
| Docker | Local database containerization |
| dotenv | Environment variable management |

### Data Flow

```Plain text
Weather API
    ↓
Extract JSON Response
    ↓
Transform/Normalize Data
    ↓
Load Into PostgreSQL
```

## What Went Well

### API Integration

The API integration process was straightforward using the requests library. Parameterized requests simplified query construction and response handling.

### Database Design

The schema design successfully enforced uniqueness using:

```sql
ON CONFLICT (location, observed_at) DO NOTHING
```

This enabled idempotent pipeline behavior.

### Docker Usage

Using Docker simplified PostgreSQL setup and created a repeatable local development environment.

## Challenges Encountered

### PostgreSQL Connectivity Issues

Encountered socket connection failures due to PostgreSQL not running locally.

Example:

```Plain text
connection to server on socket "/tmp/.s.PGSQL.5432" failed
```

Resolution:

- Verified Docker container status
- Confirmed exposed ports
- Used correct connection parameters

### Python Environment Issues

Encountered:

- missing packages
- pip path confusion
- virtual environment inconsistencies

Resolution:

- standardized .venv
- validated interpreter selection
- installed dependencies inside virtual environment

## Failure Injection Exercises

1. Invalid API Endpoint (404 Testing)

    Modified API path to intentionally trigger:

    ```Plain text
    requests.exceptions.HTTPError
    ```

    Lesson learned:

    - Difference between HTTP-level errors and connectivity failures

2. Transaction Rollback Testing

    Intentionally added:

    ```python
    conn.rollback()
    ```

    Result:

    - SQL executed successfully
    - no exception occurred
    - data was not persisted

    Lesson learned:
    - database writes are not durable until committed

## Key Technical Lessons Learned

### Transactions

Learned the importance of:

- commits
- rollbacks
- transaction boundaries
- ACID principles

### Idempotency

Using ON CONFLICT DO NOTHING prevents duplicate inserts and supports safe reruns.

### Environment Isolation

Virtual environments reduce dependency conflicts and improve reproducibility.

### Defensive Engineering

Layered exception handling improves observability and debugging.

## Security Considerations

### Good Practices Implemented

- Used parameterized SQL queries
- Stored credentials in .env
- Avoided hardcoded secrets
- Used least-privilege database user

### Future Improvements

- secrets management system
- TLS database connections
- credential rotation
- centralized logging

## Scalability Considerations

Current implementation works for small-scale ingestion but would require improvements for production-scale workloads.

### Future Enhancements

- connection pooling
- batch inserts
- retry mechanisms
- async ingestion
- Kafka/event streaming
- orchestration with Airflow
- Kubernetes deployment

## Operational/DevOps Insights

### Docker Benefits

- repeatable environments
- simplified onboarding
- environment consistency

### Observability Gaps

Current pipeline lacks:

- structured logging
- metrics
- tracing
- alerting

### Future versions should integrate

- OpenTelemetry
- Prometheus
- Grafana

## Improvements for Phase 2

Planned Enhancements

- Add structured logging
- Add retry logic
- Add unit tests
- Add integration tests
- Add metrics collection
- Add containerized application deployment
- Add CI/CD pipeline
- Add schema migrations
- Add batch processing support

## Final Thoughts

Phase 1 successfully established a foundational ETL pipeline while reinforcing core backend engineering concepts including transactions, persistence, error handling, environment management, and operational troubleshooting.

The project provided practical experience across software engineering, data engineering, and DevOps disciplines while establishing a strong baseline for future production-grade enhancements.
