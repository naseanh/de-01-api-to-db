"""
Tests for Kubernetes metrics server configuration.
"""

from pathlib import Path


def test_metrics_server_deployment_exists():
    """Verify metrics server deployment manifest exists."""

    deployment = Path("k8s/metrics-server-deployment.yaml")

    assert deployment.exists()


def test_metrics_server_service_exists():
    """Verify metrics server service manifest exists."""

    service = Path("k8s/metrics-server-service.yaml")

    assert service.exists()
