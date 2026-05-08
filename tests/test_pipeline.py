"""
Unit tests for full pipeline orchestration behavior.
"""

from unittest.mock import patch

from src.pipeline import run_pipeline

from tests.fixtures import sample_clean_weather_record, sample_raw_weather_data


@patch("src.pipeline.load")
@patch("src.pipeline.transform")
@patch("src.pipeline.extract")
def test_run_pipeline_calls_extract_transform_and_load(mock_extract, mock_transform, mock_load):
    """Verify run_pipeline() executes extract, transform, and load."""

    raw_data = sample_raw_weather_data()
    clean_record = sample_clean_weather_record()

    mock_extract.return_value = raw_data
    mock_transform.return_value = clean_record

    run_pipeline()

    mock_extract.assert_called_once_with()
    mock_transform.assert_called_once_with(raw_data)
    mock_load.assert_called_once_with(clean_record)
