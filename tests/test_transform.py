"""
Unit tests for the transform() function.

These tests validate that raw Open-Meteo API responses are normalized
into the internal record format expected by the database load step.
"""

from datetime import datetime

from src.pipeline import transform

from tests.fixtures import sample_raw_weather_data


def test_transform_returns_expected_structure():
    """Verify transform() maps raw API fields into normalized output fields."""

    raw_data = sample_raw_weather_data()

    result = transform(raw_data)

    assert result["latitude"] == 33.5018
    assert result["longitude"] == -81.9651
    assert result["temperature_c"] == 22.5
    assert result["wind_speed_kmh"] == 15.0
    assert result["observed_at"] == datetime.fromisoformat("2026-05-07T00:00")


def test_transform_converts_temperature_to_fahrenheit():
    """Verify Celsius temperature is converted to Fahrenheit."""

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 0.0,
            "windspeed": 10.0,
            "time": "2026-05-06T19:00",
        },
    }

    result = transform(raw_data)

    assert result["temperature_f"] == 32.0


def test_transform_converts_wind_speed_to_mph():
    """Verify wind speed is converted from kilometers per hour to miles per hour."""

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 20.0,
            "windspeed": 16.0934,
            "time": "2026-05-06T19:00",
        },
    }

    result = transform(raw_data)

    assert round(result["wind_speed_mph"], 1) == 10.0
