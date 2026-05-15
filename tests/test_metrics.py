"""
Unit tests for ETL metrics tracking.
"""

from src.metrics import PipelineMetrics, get_metrics_snapshot, metrics


def test_get_metrics_snapshot_returns_current_values():
    """Verify get_metrics_snapshot() returns current metric values."""

    metrics.total_runs = 2
    metrics.successful_runs = 1
    metrics.failed_runs = 1
    metrics.last_extract_duration_seconds = 0.5
    metrics.last_transform_duration_seconds = 0.1
    metrics.last_load_duration_seconds = 0.3
    metrics.last_total_duration_seconds = 0.9

    snapshot = get_metrics_snapshot()

    assert snapshot["total_runs"] == 2
    assert snapshot["successful_runs"] == 1
    assert snapshot["failed_runs"] == 1
    assert snapshot["last_extract_duration_seconds"] == 0.5
    assert snapshot["last_transform_duration_seconds"] == 0.1
    assert snapshot["last_load_duration_seconds"] == 0.3
    assert snapshot["last_total_duration_seconds"] == 0.9


def test_pipeline_metrics_defaults_to_zero():
    """Verify PipelineMetrics initializes with zeroed counters and durations."""

    metrics1 = PipelineMetrics()

    assert metrics1.total_runs == 0
    assert metrics1.successful_runs == 0
    assert metrics1.failed_runs == 0
    assert metrics1.last_extract_duration_seconds == 0.0
    assert metrics1.last_transform_duration_seconds == 0.0
    assert metrics1.last_load_duration_seconds == 0.0
    assert metrics1.last_total_duration_seconds == 0.0
