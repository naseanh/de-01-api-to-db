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

## Metrics HTTP Endpoint

The ETL platform now exposes Prometheus-style metrics through an HTTP endpoint.

Default endpoint:

```text
http://localhost:8000/metrics
```

## Kubernetes Metrics Server Deployment

The metrics endpoint can run inside Kubernetes as a separate deployment.

Apply the metrics server manifests:

```bash
kubectl apply -f k8s/metrics/
```

## Helm-Managed Metrics Server

The metrics server can also be deployed through the Helm chart.

Deploy or upgrade the Helm release:

```bash
helm upgrade --install weather-etl helm/weather-etl \
  --namespace data-pipelines \
  --create-namespace \
  --wait
```

Validate the Helm-managed metrics server resources:

```bash
kubectl get deploy,svc,pods -n data-pipelines -l app=metrics-server
```

Inspect metrics server logs:

```bash
kubectl logs -n data-pipelines -l app=metrics-server
```

Forward the metrics service locally:

```bash
kubectl port-forward svc/metrics-server 8000:8000 -n data-pipelines
```

Validate metrics exposure:

```bash
curl localhost:8000/metrics
```

Expected output:

```text
etl_total_runs
etl_successful_runs
etl_failed_runs
etl_last_total_duration_seconds
```

This Helm integration allows observability workloads to be packaged, versioned, and deployed consistently alongside the ETL platform.

## Kubernetes Metrics Endpoint Validation

Validate the metrics server pod:

```bash
kubectl get pods -n data-pipelines -l app=metrics-server
```

## Prometheus Deployment

Apply Prometheus manifests:

```bash
kubectl apply -f k8s/observability/
```

## Local Log Validation

Run:

```bash
python -m src.pipeline
```

## Current Metrics Limitation

The metrics server currently exposes in-memory metrics from the metrics-server process.

ETL Jobs run in separate short-lived Pods, so Job-level in-memory counters do not persist into the metrics-server process.

Current behavior:

- Prometheus can scrape the metrics endpoint
- Metrics endpoint returns valid Prometheus-formatted metrics
- Counters may remain at zero unless the metrics server process itself updates them

Future improvements may include:

- shared metrics persistence
- PostgreSQL-backed metrics aggregation
- Pushgateway-style metrics collection
- OpenTelemetry Collector integration
- Prometheus Pushgateway integration
