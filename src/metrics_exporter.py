"""
Prometheus-style metrics exporter utilities.
"""

from src.metrics import get_metrics_snapshot


def generate_prometheus_metrics() -> str:
    """
    Generate Prometheus-style metrics output.

    Returns:
        str: Metrics in Prometheus exposition format.
    """

    snapshot = get_metrics_snapshot()

    return f"""
# HELP etl_total_runs Total ETL pipeline runs
# TYPE etl_total_runs counter
etl_total_runs {snapshot["total_runs"]}

# HELP etl_successful_runs Successful ETL pipeline runs
# TYPE etl_successful_runs counter
etl_successful_runs {snapshot["successful_runs"]}

# HELP etl_failed_runs Failed ETL pipeline runs
# TYPE etl_failed_runs counter
etl_failed_runs {snapshot["failed_runs"]}

# HELP etl_last_extract_duration_seconds Last extract duration
# TYPE etl_last_extract_duration_seconds gauge
etl_last_extract_duration_seconds {snapshot["last_extract_duration_seconds"]}

# HELP etl_last_transform_duration_seconds Last transform duration
# TYPE etl_last_transform_duration_seconds gauge
etl_last_transform_duration_seconds {snapshot["last_transform_duration_seconds"]}

# HELP etl_last_load_duration_seconds Last load duration
# TYPE etl_last_load_duration_seconds gauge
etl_last_load_duration_seconds {snapshot["last_load_duration_seconds"]}

# HELP etl_last_total_duration_seconds Last total pipeline duration
# TYPE etl_last_total_duration_seconds gauge
etl_last_total_duration_seconds {snapshot["last_total_duration_seconds"]}
""".strip()
