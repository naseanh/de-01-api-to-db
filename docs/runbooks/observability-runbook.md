# Observability Runbook

## Objective

This runbook explains how to inspect ETL pipeline observability signals during local, Docker, Kubernetes, and Helm-based execution.

## Current Observability Signals

The ETL pipeline currently emits logs for:

- pipeline start
- extract stage duration
- transform stage duration
- load stage duration
- total pipeline duration
- successful pipeline completion
- pipeline failure context

## Current Metrics Signals

The ETL pipeline currently tracks lightweight in-memory metrics for:

- total pipeline runs
- successful pipeline runs
- failed pipeline runs
- extract stage duration
- transform stage duration
- load stage duration
- total pipeline duration

These metrics are currently logged during execution and will later become the foundation for Prometheus and OpenTelemetry integration.

## Metrics Snapshot

The pipeline exposes an internal runtime metrics snapshot that includes:

- total runs
- successful runs
- failed runs
- extract duration
- transform duration
- load duration
- total duration

The snapshot is logged at the end of each pipeline execution.

Example log:

```text
Metrics snapshot: {'total_runs': 1, 'successful_runs': 1, 'failed_runs': 0, 'last_extract_duration_seconds': 0.42, 'last_transform_duration_seconds': 0.01, 'last_load_duration_seconds': 0.18, 'last_total_duration_seconds': 0.61}
```

## Prometheus-Style Metrics Exporter

The project now includes a lightweight Prometheus-style metrics exporter.

Current exported metrics include:

| Metric | Type | Purpose |
| --- | --- | --- |
| `etl_total_runs` | counter | Total ETL pipeline executions |
| `etl_successful_runs` | counter | Successful ETL runs |
| `etl_failed_runs` | counter | Failed ETL runs |
| `etl_last_extract_duration_seconds` | gauge | Last extract stage duration |
| `etl_last_transform_duration_seconds` | gauge | Last transform stage duration |
| `etl_last_load_duration_seconds` | gauge | Last load stage duration |
| `etl_last_total_duration_seconds` | gauge | Last full pipeline duration |

The exporter currently generates Prometheus-compatible text output internally. Future work will expose these metrics through a scrapeable HTTP endpoint or OpenTelemetry exporter.

## Local Log Validation

Run:

```bash
python -m src.pipeline
```
