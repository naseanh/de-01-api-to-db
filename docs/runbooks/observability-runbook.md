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

## Local Log Validation

Run:

```bash
python -m src.pipeline
```
