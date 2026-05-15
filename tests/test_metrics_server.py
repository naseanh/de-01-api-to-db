"""
Tests for metrics HTTP server configuration.
"""

from src.metrics_server import HOST, PORT


def test_metrics_server_configuration():
    """Verify metrics server host and port configuration."""

    assert HOST == "0.0.0.0"
    assert PORT == 8000
