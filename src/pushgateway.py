"""
Push Prometheus metrics to Pushgateway.
"""

import requests

from src.metrics_exporter import generate_prometheus_metrics


PUSHGATEWAY_URL = (
    "http://pushgateway.observability.svc.cluster.local:9091"
)


def push_metrics(job_name: str = "weather-etl") -> None:
    """
    Push ETL metrics to Prometheus Pushgateway.

    Args:
        job_name: Prometheus job name.
    """

    metrics_output = generate_prometheus_metrics()

    push_response = requests.put(
        f"{PUSHGATEWAY_URL}/metrics/job/{job_name}",
        data=metrics_output,
        timeout=5,
    )

    if push_response.status_code >= 400:
        raise RuntimeError(
        f"Pushgateway error "
        f"{push_response.status_code}: "
        f"{push_response.text}"
    )
