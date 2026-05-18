# Pushgateway Roadmap

## Problem

The ETL pipeline runs as a short-lived Kubernetes Job.

Because the Job exits after completion, its in-memory metrics disappear before Prometheus can reliably scrape them.

## Current Behavior

- Metrics server exposes Prometheus-formatted metrics
- Prometheus successfully scrapes the metrics endpoint
- ETL Job metrics do not persist into the metrics server process
- Counters may remain zero

## Recommended Pattern

Use Prometheus Pushgateway for short-lived batch jobs.

The ETL Job would:

1. Run pipeline
2. Generate metrics
3. Push final metrics to Pushgateway
4. Exit cleanly
5. Prometheus scrapes Pushgateway

## Future Implementation Steps

- Add Pushgateway deployment
- Add Pushgateway service
- Add Python push logic
- Add ETL Job environment variable for Pushgateway URL
- Add tests for push payload generation
- Add Prometheus scrape config for Pushgateway
- Add Grafana dashboard panels

## Why This Matters

Pushgateway solves the short-lived Job metrics problem by allowing batch workloads to publish metrics before exiting.
