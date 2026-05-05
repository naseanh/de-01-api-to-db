# Troubleshooting Guide

## Overview

This document provides solutions to common issues encountered when running the ETL pipeline.

Use this guide to quickly diagnose and resolve problems related to:

- PostgreSQL
- Docker
- Python execution
- Environment configuration

---

## Database Issues

### Error: relation "weather_observations" does not exist

**Cause**: The database schema has not been applied to the target database.

**Fix**:

```bash
psql -h localhost -p 5433 -U pipeline_user -d pipeline_db -f sql/schema.sql
```

### Error: duplicate key value violates unique constraint

**Cause**: Attempting to insert a record that already exists.

**Fix**: This is expected behavior and handled by:

```sql
ON CONFLICT (location, observed_at) DO NOTHING;
```

No action required unless duplicates are unexpected.

## Docker Issues

### Error: container name “pipeline_postgres” is already in use

**Cause**: The container already exists.

**Fix**:

- Start the existing container.

```bash
docker start pipeline_postgres
```

- Or remove and recreate:

```bash
docker rm -f pipeline_postgres
```

### Error: cannot connect to PostgreSQL

**Cause**:

- Container is not running
- Incorrect port configuration

**Fix**:

- Check container status.

```bash
docker ps
```

- Verify port mapping:

```plain text
localhost:5433 → container:5432
```

- Ensure `.env` matches:

```bash
DB_PORT=5433
```

## Python / psycopg2 Issues

### Error: cursor already closed

**Cause**: The cursor is used outside its context manager.

**Fix**: Ensure SQL execution occurs inside.

```python
with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        cursor.execute(sql, record)
```

### Error: connection refused

**Cause**:

- PostgreSQL is not running
- Incorrect host/port

**Fix**
Check:

- Docker container is running
- `.env` values are correct

## Environemnt Issues

### Issue: `.env` variables not loading

**Cause**:

- `.env` file missing or misconfigured
- VS Code terminal not loading environment variables

**Fix**:

- Ensure .env exists in project root and includes:

```bash
DB_HOST=localhost
DB_PORT=5433
DB_NAME=pipeline_db
DB_USER=pipeline_user
DB_PASSWORD=strongpassword
```

Verify `load_dotenv()` is present in code.

### VS Code Warning: terminal environment injection is disabled

**Cause**: VS Code is not loading .env into the terminal environment.

**Fix**: Enable in settings.

```json
"python.terminal.useEnvFile": true
```

## Schema / SQL Issues

### Issue: table exists but no data

**Cause**: Pipeline has not been run successfully.

**Fix**:

- Run:

```bash
python3 src/pipeline.py
```

- Then validate:

```sql
SELECT * FROM weather_observations ORDER BY observed_at DESC LIMIT 5;
```

### Issue: new columns not appearing

**Cause**: Schema changes were not applied.

**Fix**:

- Run:

```sql
ALTER TABLE weather_observations
ADD COLUMN temperature_f DOUBLE PRECISION,
ADD COLUMN wind_speed_mph DOUBLE PRECISION;
```

## Networking Issues

### Issue: API request fails

**Cause**:

- No internet connection
- API timeout or failure

**Fix**:

- Check connectivity:

```bash
curl https://api.open-meteo.com/v1/forecast
```

- Retry running the pipeline.

## Debugging Tips

- Print environment variables to verify configuration:

```python
print(os.getenv("DB_HOST"))
```

- Check Docker logs:

```bash
docker logs pipeline_postgres
```

- Verify database connectivity manually:

```bash
psql -h localhost -p 5433 -U pipeline_user -d pipeline_db
```

## When to Escalate

If issues persist:

1. Verify all setup steps in docs/setup.md
2. Restart Docker
3. Recreate the PostgreSQL container
4. Re-run schema and pipeline from scratch
