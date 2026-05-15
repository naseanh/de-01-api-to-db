"""
Tests for Prometheus metrics exporter.
"""

from src.metrics import metrics
from src.metrics_exporter import generate_prometheus_metrics


def test_generate_prometheus_metrics_contains_expected_metrics():
    """Verify Prometheus metrics output contains expected values."""

    metrics.total_runs = 1
    metrics.successful_runs = 1
    metrics.failed_runs = 0

    output = generate_prometheus_metrics()

    assert "etl_total_runs 1" in output
    assert "etl_successful_runs 1" in output
    assert "etl_failed_runs 0" in output
