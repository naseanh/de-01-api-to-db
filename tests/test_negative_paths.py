"""
Negative-path tests for malformed or incomplete API responses.
"""

import pytest

from src.pipeline import transform


def test_transform_raises_key_error_when_current_weather_missing():
    """
    Verify transform() raises KeyError when current_weather is missing.
    """

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
    }

    with pytest.raises(KeyError):
        transform(raw_data)


def test_transform_raises_key_error_when_temperature_missing():
    """
    Verify transform() raises KeyError when temperature field is missing.
    """

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "windspeed": 15.0,
            "time": "2026-05-06T19:00",
        },
    }

    with pytest.raises(KeyError):
        transform(raw_data)


def test_transform_raises_value_error_for_invalid_timestamp():
    """
    Verify transform() raises ValueError for malformed timestamps.
    """

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 22.5,
            "windspeed": 15.0,
            "time": "INVALID_TIMESTAMP",
        },
    }

    with pytest.raises(ValueError):
        transform(raw_data)
