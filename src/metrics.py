"""
Simple in-memory ETL metrics tracking.

This module provides lightweight runtime metrics
for ETL execution visibility.
"""

from dataclasses import dataclass


@dataclass
class PipelineMetrics:
    """
    Tracks ETL pipeline execution metrics.
    """

    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0

    last_extract_duration_seconds: float = 0.0
    last_transform_duration_seconds: float = 0.0
    last_load_duration_seconds: float = 0.0
    last_total_duration_seconds: float = 0.0


metrics = PipelineMetrics()
