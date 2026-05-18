"""
Tests for Pushgateway integration.
"""

from unittest.mock import patch

from src.pushgateway import push_metrics


@patch("src.pushgateway.requests.put")
def test_push_metrics_calls_pushgateway(mock_put):
    """Verify metrics are pushed to Pushgateway."""

    mock_put.return_value.status_code = 200
    mock_put.return_value.text = ""

    push_metrics()

    assert mock_put.called
