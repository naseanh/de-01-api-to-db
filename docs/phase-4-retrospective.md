# Phase 4 Retrospective

## Overview

Phase 4 focused on deploying the ETL pipeline as a Kubernetes-managed workload.

The goal was to move beyond Docker Compose and understand how the same pipeline can run inside a Kubernetes cluster using native platform resources.

---

## Major Enhancements Completed

### Kubernetes Workload Deployment

- Added Kubernetes namespace
- Added PostgreSQL Deployment
- Added PostgreSQL Service
- Added PostgreSQL PersistentVolumeClaim
- Added PostgreSQL ConfigMap and Secret
- Added ETL Kubernetes Job
- Added schema initialization ConfigMap

### Runtime Configuration

- Replaced local `.env` dependency with Kubernetes ConfigMaps and Secrets
- Used Kubernetes DNS for service-to-service communication
- Configured the ETL Job to connect to PostgreSQL using `postgres:5432`

### Operational Documentation

- Added Kubernetes deployment runbook
- Added Kubernetes troubleshooting notes
- Updated README with Phase 4 architecture diagram
- Documented local image build requirements

---

## Challenges Encountered

### Local Image Availability

The ETL Job initially failed with `ErrImageNeverPull`.

Root cause:

- Kubernetes could not access the local Docker image
- The image name referenced by the Job did not resolve inside the cluster runtime

Resolution:

- Built the image using a local registry-style tag
- Updated the Job manifest to use `localhost:5000/weather-etl:local`
- Changed image pull behavior to support local development

### Kubernetes Job Lifecycle

The ETL workload completed quickly, which made it different from long-running services.

Lesson learned:

- ETL pipelines are better modeled as Kubernetes Jobs
- Jobs run to completion and then exit
- Logs and pod status must be inspected after completion

### Database Initialization

PostgreSQL schema initialization required understanding when `/docker-entrypoint-initdb.d/` scripts run.

Lesson learned:

- Init scripts only run during first database initialization
- Existing volumes can prevent schema scripts from re-running
- Persistent storage lifecycle matters in Kubernetes

### Service Discovery

The ETL Job connected to PostgreSQL through Kubernetes DNS.

Lesson learned:

- Applications inside Kubernetes should use Service names
- `localhost` does not refer to another Pod
- Internal service communication depends on cluster DNS

---

## Engineering Concepts Reinforced

- Kubernetes namespaces
- Pods
- Deployments
- Services
- Jobs
- ConfigMaps
- Secrets
- PersistentVolumeClaims
- Cluster DNS
- Container image availability
- Workload lifecycle
- Runtime troubleshooting
- Platform deployment patterns

---

## Final Outcome

By the end of Phase 4, the ETL pipeline successfully ran as a Kubernetes Job and connected to PostgreSQL running inside the cluster.

The project now demonstrates:

- Local Python execution
- Docker Compose execution
- Kubernetes Job execution
- Runtime configuration through Kubernetes-native resources
- Operational troubleshooting with `kubectl`
- Platform deployment readiness

---

## Remaining Opportunities

Future phases can build on this by adding:

- Helm packaging
- CronJob scheduling
- Kubernetes observability
- Prometheus metrics
- Grafana dashboards
- OpenTelemetry tracing
- CI/CD-driven Kubernetes deployment
