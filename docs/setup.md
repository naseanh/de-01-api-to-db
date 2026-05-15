# Setup Guide

## Overview

This guide walks through setting up the ETL pipeline locally, including:

- Python environment setup
- Dependency installation
- PostgreSQL container setup
- Database schema initialization
- Running the pipeline

---

## Prerequisites

Ensure the following are installed:

- Python 3.10+
- Docker
- Git
- PostgreSQL client (`psql`)
- (Optional) DataGrip or another SQL client

---

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd de-01-api-to-db
```

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

### Option A (recommended - reproduction)

```bash
pip install -r requirements.txt
```

### Option B (if updating dependencies)

```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## 4. Configure Environmental Variables

Create a `.env` file in the project root:

```bash
DB_HOST=localhost
DB_PORT=5433
DB_NAME=pipeline_db
DB_USER=pipeline_user
DB_PASSWORD=strongpassword

DEFAULT_LOCATION=Baltimore, MD
DEFAULT_LATITUDE=39.2904
DEFAULT_LONGITUDE=-76.6122

WEATHER_LOCATION=Augusta, GA
WEATHER_LATITUDE=33.4735
WEATHER_LONGITUDE=-82.0105
```

## 5. Start PostgreSQL (Docker)

If container already exists:

```bash
docker start pipeline_postgres
```

If creating fresh:

```bash
docker run -d \
  -e POSTGRES_USER=pipeline_user \
  -e POSTGRES_PASSWORD=strongpassword \
  -e POSTGRES_DB=pipeline_db \
  -p 5433:5432 \
  --name pipeline_postgres \
  postgres:15
```

## 6. Initialize Database Schema

Run the schema file:

```bash
psql -h localhost -p 5433 -U pipeline_user -d pipeline_db -f sql/schema.sql
```

## 7. Run the Pipeline

```bash
python3 -m src.pipeline
```

Expected output:

```Plain text
Pipeline complete. Location: Augusta, GA | Temp: XX.XC / XX.XF | Wind: XX.X km/h / XX.X mph | Observed: <timestamp>
```

## Validate Data

Run:

```bash
psql -h localhost -p 5433 -U pipeline_user -d pipeline_db
```

Then:

```sql
SELECT * FROM weather_observations ORDER BY observed_at DESC LIMIT 5;
```

Or use DataGrip.

## 9. Troubleshooting

Common issues:

### Port mismatch

Ensure:

```bash
DB_PORT=5433
```

Docker maps:

```code
localhost:5433 → container:5432
```

### Table does not exist

Run:

```bash
psql -h localhost -p 5433 -U pipeline_user -d pipeline_db -f sql/schema.sql
```

### Container name conflict

```bash
docker ps -a
docker rm -f pipeline_postgres
```

## Docker Compose Runtime

Start the full ETL stack:

```bash
docker compose up --build
```

Validate containers:

```bash
docker compose ps
```

Stop runtime:

```bash
docker compose down
```

## Kubernetes Runtime

Apply Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

Validate resources:

```bash
kubectl get all -n data-pipelines
```

Inspect logs:

```bash
kubectl logs -n data-pipelines -l app=weather-etl
```

## Helm Deployment

Install Helm release:

```bash
helm upgrade --install weather-etl helm/weather-etl \
  --namespace data-pipelines \
  --create-namespace \
  --wait
```

Validate release:

```bash
helm status weather-etl -n data-pipelines
```

For additional issues, see:
[Full Troubleshooting Guide](troubleshooting.md)

## Notes

- `.env` is loaded via `python-dotenv`
- `requirements.in` is the source of truth for dependencies
- `requirements.txt` is the compiled, reproducible dependency list
