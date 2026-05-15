# Phase 3 Roadmap

## Objective

Phase 3 focuses on containerizing the ETL runtime and improving local deployment repeatability using Docker and Docker Compose.

## Completed Enhancements

- Added Dockerfile for the ETL application runtime
- Added `.dockerignore`
- Added Docker Compose stack for PostgreSQL and ETL application
- Externalized runtime configuration through `.env`
- Added `.env.example` documentation
- Added PostgreSQL schema initialization through Docker Compose
- Added PostgreSQL healthcheck and startup readiness handling
- Validated full stack execution with `docker compose up --build`

## Engineering Concepts Practiced

- Containerized application runtime
- Docker image layering
- Docker Compose service orchestration
- Container-to-container networking
- Host port vs container port mapping
- Persistent volumes
- Database initialization
- Healthchecks and startup readiness
- Runtime configuration injection

## Remaining Opportunities

- Add Makefile workflow shortcuts
- Add Docker image security scanning
- Run container as a non-root user
- Add Compose profiles for manual vs automatic ETL execution
- Prepare for Kubernetes Job deployment in Phase 4
