"""
Unit tests for transform() logic.

Purpose:
Validate that raw API data is correctly normalized
into the internal pipeline record structure.
"""

from src.pipeline import transform


def test_transform_returns_expected_structure():
    """
    Ensure transform() returns normalized fields correctly.
    """

    raw_data = {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 22.5,
            "windspeed": 15.0,
            "time": "2026-05-06T19:00"
        }
    }

    result = transform(raw_data)

    assert result["latitude"] == 33.5018
    assert result["longitude"] == -81.9651
    assert result["temperature_c"] == 22.5
    assert result["wind_speed_kmh"] == 15.0
    assert result["temperature_f"] == (22.5 * 9 / 5) + 32
    assert result["wind_speed_mph"] == 15.0 * 0.621371
    assert result["observed_at"].isoformat() == "2026-05-06T19:00:00"
