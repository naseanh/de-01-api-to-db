"""
Unit tests for ETL metrics tracking.
"""

from src.metrics import PipelineMetrics


def test_pipeline_metrics_defaults_to_zero():
    """Verify PipelineMetrics initializes with zeroed counters and durations."""

    metrics = PipelineMetrics()

    assert metrics.total_runs == 0
    assert metrics.successful_runs == 0
    assert metrics.failed_runs == 0
    assert metrics.last_extract_duration_seconds == 0.0
    assert metrics.last_transform_duration_seconds == 0.0
    assert metrics.last_load_duration_seconds == 0.0
    assert metrics.last_total_duration_seconds == 0.0
