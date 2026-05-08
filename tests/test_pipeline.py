"""
Unit tests for full pipeline orchestration behavior.
"""

from unittest.mock import patch

from src.pipeline import run_pipeline


@patch("src.pipeline.load")
@patch("src.pipeline.transform")
@patch("src.pipeline.extract")
def test_run_pipeline_calls_extract_transform_and_load(mock_extract, mock_transform, mock_load):
    """Verify run_pipeline() executes extract, transform, and load."""

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 22.5,
            "windspeed": 15.0,
            "time": "2026-05-07T00:00",
        },
    }

    clean_record = {
        "location": "Augusta, GA",
        "temperature_c": 22.5,
        "temperature_f": 72.5,
        "wind_speed_kmh": 15.0,
        "wind_speed_mph": 9.3,
        "observed_at": "2026-05-07T00:00",
    }

    mock_extract.return_value = raw_data
    mock_transform.return_value = clean_record

    run_pipeline()

    mock_extract.assert_called_once_with()
    mock_transform.assert_called_once_with(raw_data)
    mock_load.assert_called_once_with(clean_record)
