"""
Tests for Helm chart rendering.

These tests validate that key Kubernetes resources render correctly
from the Helm chart.
"""

import subprocess


def test_helm_chart_lints_successfully():
    """Verify Helm lint passes for the weather-etl chart."""

    result = subprocess.run(
        ["helm", "lint", "helm/weather-etl"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_helm_template_renders_successfully():
    """Verify Helm template renders Kubernetes manifests successfully."""

    result = subprocess.run(
        ["helm", "template", "weather-etl", "helm/weather-etl"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "kind: Job" in result.stdout
    assert "kind: CronJob" in result.stdout
    assert "kind: Deployment" in result.stdout
    assert "kind: Service" in result.stdout
