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

## Environment Issues

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

## CI/CD Issues

### Issue: GitHub Actions pytest failure during CI

**Cause**:

- pytest discovered operational utility scripts as test files
- Missing required environment variables in CI
- Incorrect pytest discovery configuration

**Fix**:

- Restrict test discovery to the `tests/` directory using `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

- Ensure utility scripts do not start with test_
- Verify required packages are installed in GitHub Actions workflow

### Issue: pylint duplicate-code warning

**Cause**:

- Multiple test cases contain repeated inline mock data structures

**Fix**:

- Extract reusable fixtures or helper functions into shared test utilities

Example:

```python
def sample_raw_weather_data():
    return {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 22.5,
            "windspeed": 15.0,
            "time": "2026-05-06T19:00",
        },
    }
```

## API Retry / Timeout Issues

### Issue: API request timed out

**Cause**:

- Open-Meteo API latency
- Network instability
- Request exceeded configured timeout threshold

**Fix**:

- Verify internet connectivity
- Re-run the pipeline
- Confirm retry logic is functioning correctly
- Review logs for retry attempts and timeout messages

### Issue: Pipeline retries but still fails

**Cause**:

- External API unavailable
- Persistent DNS or connectivity issue

**Fix**:

- Validate API accessibility manually:

```bash
curl https://api.open-meteo.com/v1/forecast
```

- Check retry configuration values
- Inspect application logs for repeated failures

## Git / GitHub Issues

### Issue: Git repeatedly asks for SSH passphrase

**Cause**:

- SSH key is encrypted and not loaded into ssh-agent

**Fix**:

Start ssh-agent:

```bash
eval "$(ssh-agent -s)"
```

Add SSH key:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### Issue: Branch already exists after merge

**Cause**:

- Local branch recreated using a previously merged branch name

**Fix**:

- Rename local branch:

```bash
git branch -m new-branch-name
```

- Push upstream:

```bash
git push -u origin HEAD
```

### Issue: GitHub Actions workflow does not trigger

**Cause**:

- Branch already merged
- No new commits pushed
- Workflow YAML syntax issue

**Fix**:

- Create a new commit:

```bash
git commit --allow-empty -m "chore: retrigger workflow"
git push
```

- Verify workflow syntax in .github/workflows/

## Docker Compose Issues

### Issue: container name is already in use

**Cause**: A previous standalone Docker container already exists with the same name.

**Fix**:

```bash
docker rm -f pipeline_postgres
```

Or remove fixed container_name values from docker-compose.yml.

**Issue**: app connects to postgres on the wrong port

**Cause**: Local host uses mapped port 5433, but containers communicate internally on port `5432`.

**Fix**:

```yaml
DB_HOST: postgres
DB_PORT: "5432"
```

**Issue**: relation “weather_observations” does not exist

**Cause**: The schema was not initialized in the Compose PostgreSQL volume.

**Fix**:

```bash
docker compose down -v
docker compose up --build
```

**Issue**: schema initialization fails

**Cause**: schema.sql contains duplicate column creation or non-idempotent SQL.

**Fix**: Ensure columns are defined once in CREATE TABLE and avoid duplicate ALTER TABLE statements.

**Issue**: ETL starts before PostgreSQL is ready

**Cause**: depends_on controls start order, not readiness.

**Fix**: Add a PostgreSQL healthcheck and use:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

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
