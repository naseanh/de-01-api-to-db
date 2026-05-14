# Helm Deployment Runbook

## Objective

Deploy the ETL pipeline into Kubernetes using Helm packaging and release management workflows.

---

## Build Local Kubernetes Image

Build the ETL image locally before deployment.

```bash
docker build -t localhost:5000/weather-etl:local .
```
