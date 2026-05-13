# Phase 3 Retrospective

## Overview

Phase 3 moved the ETL pipeline from a local Python runtime into a containerized runtime using Docker and Docker Compose.

The goal was to make the project more portable, repeatable, and deployment-ready.

## What Changed

- Added an application Dockerfile
- Added Docker Compose orchestration
- Ran PostgreSQL and the ETL application as services
- Used Docker networking for service-to-service communication
- Mounted schema initialization into PostgreSQL
- Added startup readiness using PostgreSQL healthchecks
- Improved environment configuration examples

## Challenges Encountered

### Container Name Conflicts

A previous standalone PostgreSQL container conflicted with Compose-managed containers.

Lesson learned: avoid fixed `container_name` values unless necessary.

### Host Port vs Container Port Confusion

The host used `5433`, but containers communicate internally over `5432`.

Lesson learned: host-to-container and container-to-container networking are different execution contexts.

### Missing Database Schema

The ETL application reached PostgreSQL but failed because the table did not exist.

Lesson learned: database initialization is part of runtime orchestration.

### Schema Initialization Failure

Duplicate schema changes caused PostgreSQL initialization to fail.

Lesson learned: schema files should be clean, repeatable, and initialization-safe.

### Startup Readiness

The ETL app can start before PostgreSQL is ready unless healthchecks are configured.

Lesson learned: service start order is not the same as service readiness.

## Engineering Concepts Reinforced

- Runtime portability
- Container networking
- Docker image construction
- Persistent database volumes
- Environment-driven configuration
- Database initialization
- Healthchecks
- Startup sequencing
- Operational debugging

## Final Outcome

By the end of Phase 3, the project could run as a containerized ETL stack using Docker Compose.

The application and database now run together in a reproducible local runtime environment, creating a strong foundation for future Kubernetes deployment.
