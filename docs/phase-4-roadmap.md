# Phase 4 Roadmap

## Objective

Phase 4 focuses on deploying the ETL pipeline as a Kubernetes-managed workload.

The goal is to move from Docker Compose orchestration to Kubernetes job-based execution.

## Primary Goals

- Deploy PostgreSQL and the ETL application into Kubernetes
- Run the ETL pipeline as a Kubernetes Job
- Externalize configuration using ConfigMaps and Secrets
- Add Kubernetes health/readiness concepts
- Practice `kubectl` troubleshooting workflows
- Document the deployment process

## Planned Enhancements

- Kubernetes namespace
- PostgreSQL Deployment
- PostgreSQL Service
- PostgreSQL PersistentVolumeClaim
- ETL ConfigMap
- ETL Secret
- ETL Kubernetes Job
- Kubernetes troubleshooting guide
- Phase 4 retrospective

## Engineering Concepts Practiced

- Kubernetes Pods
- Deployments
- Services
- Jobs
- ConfigMaps
- Secrets
- PersistentVolumeClaims
- Cluster DNS
- Workload lifecycle
- Runtime troubleshooting

## Success Criteria

Phase 4 is complete when:

- PostgreSQL runs inside Kubernetes
- The ETL app runs as a Kubernetes Job
- The ETL Job connects to PostgreSQL through Kubernetes DNS
- The pipeline inserts weather data successfully
- Logs can be inspected with `kubectl logs`
- Data can be verified with `kubectl exec`
