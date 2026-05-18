# Kubernetes Deployment Runbook

## Objective

Deploy the ETL pipeline into Kubernetes as a job-based workload.

## Build Local Kubernetes Image

Build the ETL image locally so the Kubernetes cluster can access it.

```bash
docker build -t localhost:5000/weather-etl:local .
```

## Apply Manifests

```bash
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/postgres/
kubectl apply -f k8s/etl/
kubectl apply -f k8s/metrics/
kubectl apply -f k8s/observability
```

## Check Resources

```bash
kubectl get all -n data-pipelines
kubectl get pvc -n data-pipelines
kubectl get pods -n data-pipelines
```

## Check PostgreSQL Readiness

```bash
kubectl get pods -n data-pipelines -l app=postgres
kubectl describe pod -n data-pipelines -l app=postgres
```

## Check ETL Job

```bash
kubectl get jobs -n data-pipelines
kubectl get pods -n data-pipelines -l app=weather-etl
```

## View ETL Logs

```bash
kubectl logs -n data-pipelines -l app=weather-etl
```

## Verify Data

```bash
kubectl exec -it -n data-pipelines deploy/postgres -- \
  psql -U pipeline_user -d pipeline_db
```

Then run:

```sql
SELECT *
FROM weather_observations
ORDER BY observed_at DESC
LIMIT 5;
```

## Cleanup

```bash
kubectl delete namespace data-pipelines
```
