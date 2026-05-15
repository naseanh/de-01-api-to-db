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

## Local Log Validation

Run:

```bash
python src/pipeline.py
```
