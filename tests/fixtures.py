"""
Reusable test fixtures for pipeline unit tests.
"""


def sample_raw_weather_data():
    """Return sample raw Open-Meteo API response data."""

    return {
        "latitude": 33.5018,
        "longitude": -81.9651,
        "current_weather": {
            "temperature": 22.5,
            "windspeed": 15.0,
            "time": "2026-05-07T00:00",
        },
    }


def sample_clean_weather_record():
    """Return sample transformed weather record."""

    return {
        "location": "Augusta, GA",
        "temperature_c": 22.5,
        "temperature_f": 72.5,
        "wind_speed_kmh": 15.0,
        "wind_speed_mph": 9.3,
        "observed_at": "2026-05-07T00:00",
    }
